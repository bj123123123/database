import os
import re
import requests
from xml.etree import ElementTree as ET


class FundManager:
    # 全局变量1: 存放基金代码的一个list
    fund_codes = []
    # 全局变量2: 一个字典，key是基金代码，value是基金净值
    fund_values = {}
    
    def __init__(self):
        """初始化函数，初始化全局变量1和全局变量2"""
        self.fund_codes = []
        self.fund_values = {}
        
        # 如果存在fundvalue.txt文件，清空fundvalue.txt文件
        if os.path.exists('fundvalue.txt'):
            with open('fundvalue.txt', 'w', encoding='utf-8') as f:
                f.write('')
        
        # 如果fund_tmp/下存在文件，删除fund_tmp/下所有文件
        if os.path.exists('fund_tmp'):
            for file in os.listdir('fund_tmp'):
                file_path = os.path.join('fund_tmp', file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            # 如果fund_tmp目录不存在，创建它
            os.makedirs('fund_tmp')
    
    def read_fund_list(self):
        """第一个函数：读取本地的文件fundlist.txt，每一行是一个基金代码，把不重复的存放到全局变量1中"""
        try:
            with open('fundlist.txt', 'r', encoding='utf-8') as f:
                codes = f.read().strip().split('\n')
                # 去重并添加到全局变量1中
                self.fund_codes = list(set(code.strip() for code in codes if code.strip()))
            return True
        except FileNotFoundError:
            print("fundlist.txt文件不存在")
            return False
    
    def fetch_fund_data(self, fund_code):
        """第二个函数：抓取网页内容，获取基金净值"""
        url = f"https://fund.eastmoney.com/{fund_code}.html"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            content = response.text
            
            # 查找<div class="dataOfFund">和</div>之间的内容
            pattern = r'<div class="dataOfFund">(.*?)</div>'
            match = re.search(pattern, content, re.DOTALL)
            
            if not match:
                print(f"基金代码：{fund_code}，抓取失败！！！")
                return False
            
            content1 = match.group(1)
            
            # 从内容1中删除"<!--"和"-->"之间的内容
            content2 = re.sub(r'<!--.*?-->', '', content1, flags=re.DOTALL)
            
            # 生成xml文件
            xml_filename = f"fund_tmp/{fund_code}.xml"
            root = ET.Element("fund_data")
            root.text = content2.strip()
            tree = ET.ElementTree(root)
            tree.write(xml_filename, encoding='utf-8', xml_declaration=True)
            
            # 在内容2中找到第一个<dd class="dataNums">和</dd>之间的内容
            pattern_dd = r'<dd class="dataNums">(.*?)</dd>'
            match_dd = re.search(pattern_dd, content2, re.DOTALL)
            
            if not match_dd:
                print(f"基金代码：{fund_code}，未找到净值数据")
                self.fund_values[fund_code] = 0
                return False
            
            content3 = match_dd.group(1)
            
            # 在内容3中把<span>和</span>之间的内容取出来（包括有class属性的span标签）
            pattern_span = r'<span[^>]*>(.*?)</span>'
            span_matches = re.findall(pattern_span, content3)
            
            if len(span_matches) >= 1:
                net_value = span_matches[0].strip()
                
                # 检查净值是否为数字
                try:
                    float(net_value)
                    self.fund_values[fund_code] = net_value
                except ValueError:
                    self.fund_values[fund_code] = "0"
            else:
                self.fund_values[fund_code] = "0"
            
            return True
            
        except requests.RequestException as e:
            print(f"基金代码：{fund_code}，抓取失败！！！")
            return False
        except Exception as e:
            print(f"基金代码：{fund_code}，处理数据时出错：{str(e)}")
            return False
    
    def fetch_all_funds(self):
        """第三个函数：循环遍历全局变量1，取出每一个基金代码，调用第二个函数"""
        for fund_code in self.fund_codes:
            self.fetch_fund_data(fund_code)
        
        # 遍历完成后，把全局变量2写入到一个txt文件中
        with open('fundvalue.txt', 'w', encoding='utf-8') as f:
            for fund_code, value in self.fund_values.items():
                f.write(f"{fund_code}\t{value}\n")
    
    def print_fund_values(self):
        """第四个函数：打印全局变量2"""
        for fund_code, value in self.fund_values.items():
            print(f"{fund_code}:{value}")


def main():
    """main函数：生成这个类的实例，调用第一个函数，然后调用第三个函数"""
    fund_manager = FundManager()
    
    # 调用第一个函数
    if fund_manager.read_fund_list():
        # 调用第三个函数
        fund_manager.fetch_all_funds()
        print("成功完成")
    else:
        print("程序执行失败")


if __name__ == "__main__":
    main()
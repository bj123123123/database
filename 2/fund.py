import os
import requests
import re
import xml.etree.ElementTree as ET
from xml.dom import minidom

class FundDataCollector:
    # 全局变量1: 存放基金代码的list
    fund_codes = []
    # 全局变量2: 字典，key是基金代码，value是基金净值
    fund_values = {}
    
    def __init__(self):
        """初始化函数"""
        # 清空全局变量
        FundDataCollector.fund_codes = []
        FundDataCollector.fund_values = {}
        
        # 如果存在fundvalue.txt文件，清空它
        if os.path.exists('fundvalue.txt'):
            with open('fundvalue.txt', 'w', encoding='utf-8') as f:
                f.write('')
        
        # 如果fund_tmp/下存在文件，删除所有文件
        if os.path.exists('fund_tmp'):
            for file in os.listdir('fund_tmp'):
                file_path = os.path.join('fund_tmp', file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        else:
            # 如果目录不存在，创建它
            os.makedirs('fund_tmp')
    
    def read_fund_list(self):
        """第一个函数：读取本地的文件fundlist.txt"""
        try:
            with open('fundlist.txt', 'r', encoding='utf-8') as f:
                for line in f:
                    code = line[1:].strip()
                    if code and code not in FundDataCollector.fund_codes:
                        FundDataCollector.fund_codes.append(code)
            print(f"成功读取 {len(FundDataCollector.fund_codes)} 个基金代码")
        except FileNotFoundError:
            print("错误：fundlist.txt 文件不存在")
        except Exception as e:
            print(f"读取fundlist.txt时发生错误: {e}")
    
    def fetch_fund_data(self, fund_code):
        """第二个函数：抓取网页内容并解析基金净值"""
        url = f"https://fund.eastmoney.com/{fund_code}.html"
        
        try:
            # 发送HTTP请求
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            response.encoding = 'utf-8'
            
            # 获取网页内容
            html_content = response.text
            
            # 查找<div class="dataOfFund">和</div>之间的内容（内容1）
            pattern = r'<div class="dataOfFund">(.*?)</div>'
            match = re.search(pattern, html_content, re.DOTALL)
            
            if not match:
                print(f"基金代码：{fund_code}，抓取失败！！！")
                return False
            
            content1 = match.group(1)
            
            # 删除<!--和-->之间的内容（得到内容2）
            content2 = re.sub(r'<!--.*?-->', '', content1, flags=re.DOTALL)
            
            # 生成XML格式的文件
            xml_content = f'<?xml version="1.0" encoding="UTF-8"?>\n<fundData>\n{content2}\n</fundData>'
            
            # 格式化XML
            try:
                dom = minidom.parseString(xml_content)
                pretty_xml = dom.toprettyxml(indent="  ")
            except:
                pretty_xml = xml_content
            
            # 保存XML文件
            xml_filename = f"fund_tmp/{fund_code}.xml"
            with open(xml_filename, 'w', encoding='utf-8') as f:
                f.write(pretty_xml)
            
            # 在内容2中找到第一个<dd class="dataNums">和</dd>之间的内容（内容3）
            dd_pattern = r'<dd class="dataNums">(.*?)</dd>'
            dd_match = re.search(dd_pattern, content2, re.DOTALL)
            
            if not dd_match:
                print(f"基金代码：{fund_code}，未找到净值数据")
                FundDataCollector.fund_values[fund_code] = 0
                return False
            
            content3 = dd_match.group(1)
            
            # 在内容3中找到<span>和</span>之间的内容（包括有属性的span标签）
            span_pattern = r'<span[^>]*>(.*?)</span>'
            span_matches = re.findall(span_pattern, content3)
            
            if len(span_matches) >= 1:
                # 第一个值是净值
                net_value = span_matches[0].strip()
                
                # 检查净值是否为数字
                try:
                    # 尝试转换为浮点数
                    float_value = float(net_value)
                    FundDataCollector.fund_values[fund_code] = float_value
                    print(f"基金代码：{fund_code}，净值：{float_value}")
                except ValueError:
                    # 如果不是数字，设置为0
                    FundDataCollector.fund_values[fund_code] = 0
                    print(f"基金代码：{fund_code}，净值格式错误，设置为0")
            else:
                FundDataCollector.fund_values[fund_code] = 0
                print(f"基金代码：{fund_code}，未找到净值数据，设置为0")
            
            return True
            
        except requests.RequestException as e:
            print(f"基金代码：{fund_code}，抓取失败！！！")
            FundDataCollector.fund_values[fund_code] = 0
            return False
        except Exception as e:
            print(f"基金代码：{fund_code}，处理时发生错误：{e}")
            FundDataCollector.fund_values[fund_code] = 0
            return False
    
    def process_all_funds(self):
        """第三个函数：循环遍历全局变量1，调用第二个函数"""
        success_count = 0
        total_count = len(FundDataCollector.fund_codes)
        
        print(f"开始处理 {total_count} 个基金...")
        
        for fund_code in FundDataCollector.fund_codes:
            if self.fetch_fund_data(fund_code):
                success_count += 1
        
        # 把全局变量2写入到fundvalue.txt文件中
        try:
            with open('fundvalue.txt', 'w', encoding='utf-8') as f:
                for code, value in FundDataCollector.fund_values.items():
                    f.write(f"A{code}\t{value}\n")
            
            print(f"处理完成！成功：{success_count}/{total_count}，结果已保存到fundvalue.txt")
        except Exception as e:
            print(f"写入fundvalue.txt时发生错误: {e}")
    
    def print_fund_values(self):
        """第四个函数：打印全局变量2"""
        print("\n基金净值数据：")
        for code, value in FundDataCollector.fund_values.items():
            print(f"{code}:{value}")

def main():
    """main函数"""
    print("开始基金数据收集程序...")
    
    # 生成类的实例
    collector = FundDataCollector()
    
    # 调用第一个函数
    collector.read_fund_list()
    
    # 调用第三个函数
    collector.process_all_funds()
    
    # 调用第四个函数，打印结果
    collector.print_fund_values()
    
    print("\n基金数据收集程序执行完成！")

if __name__ == "__main__":
    main()
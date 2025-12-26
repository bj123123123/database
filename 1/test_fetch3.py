import requests
import re

fund_code = '003095'
url = f'https://fund.eastmoney.com/{fund_code}.html'
print(f'访问URL: {url}')

try:
    response = requests.get(url, timeout=10)
    print(f'状态码: {response.status_code}')
    
    # 查找div class='dataOfFund'
    pattern = r'<div class="dataOfFund">(.*?)</div>'
    match = re.search(pattern, response.text, re.DOTALL)
    
    if match:
        print('找到dataOfFund div')
        content1 = match.group(1)
        
        # 从内容1中删除"<!--"和"-->"之间的内容
        content2 = re.sub(r'<!--.*?-->', '', content1, flags=re.DOTALL)
        print(f'内容2长度: {len(content2)}')
        
        # 在内容2中找到第一个<dd class="dataNums">和</dd>之间的内容
        pattern_dd = r'<dd class="dataNums">(.*?)</dd>'
        match_dd = re.search(pattern_dd, content2, re.DOTALL)
        
        if match_dd:
            content3 = match_dd.group(1)
            print(f'内容3: {content3}')
            
            # 修改：匹配包括class属性的span标签
            pattern_span = r'<span[^>]*>(.*?)</span>'
            span_matches = re.findall(pattern_span, content3)
            print(f'span匹配结果: {span_matches}')
            
            if len(span_matches) >= 1:
                net_value = span_matches[0].strip()
                print(f'净值: {net_value}')
                
                # 检查净值是否为数字
                try:
                    float(net_value)
                    print(f'净值是有效数字: {net_value}')
                except ValueError:
                    print(f'净值不是数字，使用0')
            else:
                print('未找到span标签')
        else:
            print('未找到dd class="dataNums"')
    else:
        print('未找到dataOfFund div')

except Exception as e:
    print(f'错误: {e}')
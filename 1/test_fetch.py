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
        content1 = match.group(1)[:200]  # 只显示前200字符
        print(f'内容1前200字符: {content1}')
    else:
        print('未找到dataOfFund div')
        # 让我们看看实际的HTML结构
        print('实际HTML中的相关部分:')
        lines = response.text.split('\n')
        for i, line in enumerate(lines):
            if 'dataOfFund' in line:
                print(f'行 {i}: {line.strip()}')
                break

except Exception as e:
    print(f'错误: {e}')
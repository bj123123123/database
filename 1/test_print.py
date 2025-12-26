from fund import FundManager

# 创建实例并打印基金净值
fund_manager = FundManager()
fund_manager.read_fund_list()  # 读取基金列表
fund_manager.fetch_all_funds()  # 获取所有基金数据
print("=== 所有基金净值 ===")
fund_manager.print_fund_values()  # 打印所有基金净值
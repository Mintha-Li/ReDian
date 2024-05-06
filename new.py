from openpyxl import Workbook

from systemfunc import create_table_header

    # # 保存工作簿
    # wb.save(output_file)

# 测试代码
platforms = ['微博', '知乎', '抖音']
num_ranks = 5
create_table_header(platforms, num_ranks, "platforms.xlsx")

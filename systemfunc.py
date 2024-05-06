import os
from datetime import datetime
from extract_top_ranking import extract_top_rankings
from openpyxl import Workbook


def process_files_in_folder(folder_path, output_folder,platforms = ['微博', '知乎', '抖音'],num_ranks = 3,source_column = 'source',rank_column = 'rank'):
    # 获取目标文件夹中的所有文件名
    file_names = os.listdir(folder_path)

    wb = Workbook()
    ws = wb.active
    # create_table_header(wb,platforms, num_ranks)

    # ws.insert_cols(1)
    # ws.merge_cells('A1:A2')

    # 表头信息
    header = ['平台']
    for platform in platforms:
        header.extend([platform] * num_ranks)

    # 添加表头和子表头
    for idx, value in enumerate(header, start=1):
        ws.cell(row=1, column=idx, value=value)

    # 在第二行第二列写入 '排名'
    ws.cell(row=2, column=1, value='排名')

    # 添加排名
    for col_idx in range(2, ws.max_column+1, (num_ranks)):
        for i in range(1, num_ranks+1):
            ws.cell(row=2, column=col_idx+i-1, value=i)

    # 合并单元格
    for col_idx in range(2, ws.max_column+1, (num_ranks)):
        ws.merge_cells(start_row=1, start_column=col_idx, end_row=1, end_column=col_idx+num_ranks-1)



    # 遍历每个文件名
    for file_name in file_names:
        # 构建文件的完整路径
        file_path = os.path.join(folder_path, file_name)
        
        # 检查文件是否为 Excel 文件
        if file_name.endswith('.xlsx'):

            top_combined = extract_top_rankings(file_path, source_column, rank_column,num_ranks,platforms=platforms)
            print(top_combined)

            
            #写入热搜标题
            ws.append(['标题'] + list(top_combined['title']))

            # 写入热度
            ws.append(['热度'] + list(top_combined['hot_num']))

            # 写入类型
            ws.append(['类型'])

    # 获取当前时间并格式化为字符串，作为文件名的一部分
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # 构建输出文件路径
    output_file_name = f"{current_time}_{'热点.xlsx'}"
    output_file_path = os.path.join(output_folder, output_file_name)
    wb.save(output_file_path)
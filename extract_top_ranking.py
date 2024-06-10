import pandas as pd

def extract_top_rankings(input_file, source_column, rank_column,rank_num=3,platforms = ['微博', '知乎', '抖音']):
    """
    提取各平台的前rank_num条数据,并将热度值格式化为“xx万”。

    参数:
    input_file (str): 输入的Excel文件路径。
    source_column (str): 平台列的列名。
    rank_column (str): 排名列的列名。
    rank_num (int): 每个平台提取的前几名数据。
    platforms (list): 要处理的平台列表。

    返回:
    pd.DataFrame: 格式化后的数据框。
    """

    # 读取Excel文件
    df = pd.read_excel(input_file)

    # 初始化空的数据框，用于存储结果
    top = pd.DataFrame()

    # 遍历每个平台，提取前rank_num条数据
    for platform in platforms:
        platform_data = df[df[source_column] == platform].nsmallest(rank_num, rank_column)
        top = pd.concat([top, platform_data])

    # 重置索引
    top_combined = top.reset_index(drop=True)

    # 根据平台对热度值进行格式化
    top_combined['hot_num'] = top_combined.apply(lambda row: convert_to_wan_format(row['hot_num'], row[source_column]), axis=1)

    return top_combined

def convert_to_wan_format(hot_num, source):
    """
    将热度值格式化为“xx万”。
    
    参数:
    hot_num (str/int/float): 热度值。
    source (str): 数据来源平台。
    
    返回:
    str: 格式化后的热度值。
    """
    if source == '知乎':
        # 移除“ 万热度”并保留“xx万”部分
        if ' 万热度' in hot_num:
            return hot_num.replace(' 万热度', '万')
    elif isinstance(hot_num, (int, float)):
        # 将微博和抖音的热度值转换为“xx万”格式
        return f"{hot_num / 10000:.0f}万" if hot_num >= 10000 else f"{hot_num}"
    return hot_num

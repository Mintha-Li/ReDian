import pandas as pd

def extract_top_rankings(input_file, source_column, rank_column,rank_num=3,platforms = ['微博', '知乎', '抖音']):
    df = pd.read_excel(input_file)
    top = pd.DataFrame()
    for platform in platforms:
        platform_data = df[df[source_column] == platform].nsmallest(rank_num, rank_column)
        top = pd.concat([top, platform_data])
    top_combined = top.reset_index(drop=True)
    return top_combined
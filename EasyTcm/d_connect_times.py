import pandas as pd


def connect_similarity(df, col1, col2):
    """
    计算给定DataFrame中两列的connect相似系数。

    参数:
        df (pd.DataFrame): 包含数据的DataFrame。
        col1 (str): 第一列的名称。
        col2 (str): 第二列的名称。

    返回:
        float: 两列之间的connect相似系数。
    """
    # 确保列存在
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError("指定的列名不在DataFrame中")

    # 计算交集大小
    intersection = ((df[col1] == 1) & (df[col2] == 1)).sum()

    # 计算connect相似系数

    return {'Item1': col1, 'Item2': col2, 'connect': intersection}


def calculate_and_save_connect_similarities(file_path, output_path, sheet_name='Sheet1'):
    """
    计算DataFrame中所有列对之间的connect相似系数，按降序排序并保存到新的Excel文件。

    参数:
        file_path (str): 输入Excel文件路径。
        output_path (str): 输出Excel文件路径。
        sheet_name (str): Excel工作表的名称，默认为'Sheet1'。
    """
    # 读取Excel文件
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # 列名列表
    columns = df.columns.tolist()

    # 存储所有列对的connect相似系数
    similarities = []

    # 计算所有列对之间的connect相似系数
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            col1 = columns[i]
            col2 = columns[j]
            similarity = connect_similarity(df, col1, col2)
            similarities.append(similarity)

    # 将结果转换为DataFrame
    result_df = pd.DataFrame(similarities)

    # 按照连接度从大到小排序
    result_df_sorted = result_df.sort_values(by='connect', ascending=False).reset_index(drop=True)

    # 保存到新的Excel文件
    result_df_sorted.to_excel(output_path, index=False)

    print(f"结果已保存至: {output_path}")




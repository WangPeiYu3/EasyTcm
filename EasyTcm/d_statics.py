import pandas as pd

def count_ones_in_columns(input_file, output_file, sheet_name='Sheet1'):
    """
    读取指定的Excel文件，统计每一列中值为1的数量，并将结果按'times'列从大到小排序后保存到新的Excel文件中。

    参数:
    input_file (str): 输入Excel文件的路径。
    output_file (str): 输出Excel文件的路径。
    sheet_name (str): 要处理的工作表名称，默认为'Sheet1'。

    返回:
    pandas.DataFrame: 包含每列名称及其对应1的数量的结果DataFrame。
    """
    try:
        # 读取Excel文件
        df = pd.read_excel(input_file, sheet_name=sheet_name)

        # 统计每一列中1的数量
        ones_count = df.apply(lambda col: (col == 1).sum())

        # 创建一个新的DataFrame来存储结果
        result_df = pd.DataFrame({
            'Item3': ones_count.index,
            'times': ones_count.values
        })

        # 按'times'列从大到小排序
        result_df_sorted = result_df.sort_values(by='times', ascending=False)

        # 将排序后的结果保存到新的Excel文件
        result_df_sorted.to_excel(output_file, index=False)

        print(f"统计结果已保存到 {output_file}")
        return result_df_sorted

    except Exception as e:
        print(f"发生错误: {e}")
        return None


def get_high_times(src_file, times):
    """
    从 Excel 文件中提取满足 times 大于指定值的 item3 列的数据，并存入数组返回。

    参数：
    - src_file: Excel 文件路径
    - times: 阈值

    返回：
    - 满足条件的 item3 数组
    """
    # 读取 Excel 文件
    df = pd.read_excel(src_file)

    # 提取满足条件的行
    high_times_rows = df[df['times'] > times]

    # 提取 item3 列并存入数组
    high_times_item3 = high_times_rows['Item3'].tolist()

    return high_times_item3


def get_top_items(input_file, output_file, row_index=19):
    """
    从输入的Excel文件中获取第row_index行的times值，
    筛选出所有times大于等于该值的行，并将结果保存到新的Excel文件。

    参数:
        input_file (str): 输入Excel文件路径。
        output_file (str): 输出Excel文件路径。
        row_index (int): 用于比较的行索引，默认为19（对应第二十行）。
    """
    # 读取Excel文件
    df = pd.read_excel(input_file, sheet_name='Sheet1')

    # 获取第row_index行的times值
    threshold_times = df.at[row_index, 'times']

    # 筛选出所有times大于等于该值的行
    filtered_df = df[df['times'] >= threshold_times]

    # 保存结果到新的Excel文件
    filtered_df.to_excel(output_file, index=False)
    print(f"结果已保存至: {output_file}")

# 示例调用


if __name__ == "__main__":
    input_file_path = 'step4.统计矩阵归经_10矩阵.xlsx'
    output_file_path = '统计结果.xlsx'
    result = count_ones_in_columns(input_file_path, output_file_path, sheet_name='Sheet1')

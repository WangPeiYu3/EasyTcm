from a_med_stand import read_excel_to_dict_list, save_dict_list_to_excel
import os
import sys
import pandas as pd


def get_col_items(col_name_, dict_list):
    dst_unique = []
    for dict_v in dict_list:
        item_list = str(dict_v[col_name_]).split("、")
        if str(dict_v[col_name_]) == 'nan':
            item_list = []
        for item_v in item_list:
            if item_v not in dst_unique:
                dst_unique.append(item_v)
    return dst_unique


def creat_rect(src_file, col_names, dst_file_v, dst_file_s, type_file):
    dst_file_list = []

    if not os.path.exists(src_file):
        print(f"源文件_{src_file}:不存在，退出程序。")
        sys.exit()
    chu_fang_list = read_excel_to_dict_list(src_file)

    if len(col_names) == 0:
        print(f"源文件_{src_file}:无数据，退出程序。")
        sys.exit()

    keys_list = list(chu_fang_list[0].keys())
    for src_column in col_names:
        if src_column not in keys_list:
            print(f'{src_file}源文件无{src_column}特征，请重试！')
            sys.exit()

    unique_items = []
    for col_name in col_names:
        unique_items += get_col_items(col_name, chu_fang_list)

    dst_dict_v_list = []
    dst_dict_s_list = []

    for chu_fang in chu_fang_list:
        dict_v = {}
        dict_s = {}
        key_list = []
        cur_ = []

        for col_name in col_names:
            cur_ += str(chu_fang[col_name]).split("、")
            if str(chu_fang[col_name]) == 'nan':
                cur_ = []

        for key_ in unique_items:
            if key_ in cur_:
                dict_v[key_] = 1
                dict_s[key_] = 'Y'
            else:
                dict_v[key_] = 0
                dict_s[key_] = 'N'

        dst_dict_v_list.append(dict_v)
        dst_dict_s_list.append(dict_s)
    if '统计矩阵' in src_file:
        pass
    else:
        save_dict_list_to_excel(dst_dict_v_list, dst_file_v)
        save_dict_list_to_excel(dst_dict_s_list, dst_file_s)
        dst_file_list.append(dst_file_v)
        dst_file_list.append(dst_file_s)

    dict_type_list = []

    for col_name in col_names:
        dst_file_v = src_file.replace('.xlsx', f'_{col_name}_10矩阵.xlsx')
        dst_file_s = src_file.replace('.xlsx', f'_{col_name}_YN矩阵.xlsx')
        unique_items = get_col_items(col_name, chu_fang_list)
        dst_dict_v_list = []
        dst_dict_s_list = []
        for chu_fang in chu_fang_list:
            cur_ = str(chu_fang[col_name]).split("、")
            if str(chu_fang[col_name]) == 'nan':
                cur_ = []
            dict_v = {}
            dict_s = {}

            for key_ in unique_items:
                if key_ in cur_:
                    dict_v[key_] = 1
                    dict_s[key_] = 'Y'
                else:
                    dict_v[key_] = 0
                    dict_s[key_] = 'N'

            dst_dict_v_list.append(dict_v)
            dst_dict_s_list.append(dict_s)

        keys_list = list(dst_dict_s_list[0].keys())
        for ke in keys_list:
            dict_type = {'Item3': ke, 'type': col_name}
            dict_type_list.append(dict_type)

        save_dict_list_to_excel(dst_dict_v_list, dst_file_v)
        save_dict_list_to_excel(dst_dict_s_list, dst_file_s)
        dst_file_list.append(dst_file_v)
        dst_file_list.append(dst_file_s)
    if '统计矩阵' in src_file:
        pass
    else:
        save_dict_list_to_excel(dict_type_list, type_file)
        dst_file_list.append(type_file)
    return dst_file_list



def extract_high_freq_columns(matrix_file, freq_stats_file, output_file):
    # 读取频次统计文件
    freq_df = pd.read_excel(freq_stats_file)

    # 提取高频药物名称列表
    high_freq_drugs = freq_df['Item3'].tolist()

    # 读取矩阵文件
    matrix_df = pd.read_excel(matrix_file, header=None)

    # 假设第一行是列名，如果不是，请调整代码以适应实际情况
    # 并将列名转换为字符串以便匹配
    matrix_columns = matrix_df.iloc[0].astype(str).tolist()
    matrix_df.columns = matrix_columns  # 将第一行设置为列名
    matrix_df = matrix_df.drop(0)  # 删除原来的索引行

    # 筛选出存在于高频药物列表中的列
    filtered_df = matrix_df.loc[:, matrix_df.columns.isin(high_freq_drugs)]

    # 保存新的高频矩阵到文件
    filtered_df.to_excel(output_file, index=False)

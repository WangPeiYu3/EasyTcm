from a_med_stand import read_excel_to_dict_list, save_dict_list_to_excel
import pandas as pd
import os
import sys


def translate_feature(src_file, dst_file, src_column, judge_colum, translate_columns, judge_file, only_one=True):
    # 检查文件是否存在
    if not os.path.exists(src_file):
        print(f"文件 '{src_file}' 不存在，程序即将退出。")
        sys.exit()

    # 检查文件是否存在
    if not os.path.exists(judge_file):
        print(f"文件 '{judge_file}' 不存在，程序即将退出。")
        sys.exit()

    src_data_list = read_excel_to_dict_list(src_file)
    judge_data_list = read_excel_to_dict_list(judge_file)
    judge_df = pd.read_excel(judge_file)

    if len(src_data_list) == 0:
        print(f'{src_file}源文件无数据，请重试！')
        sys.exit()

    if len(judge_data_list) == 0:
        print(f'{judge_file}转换文件无数据，请重试！')
        sys.exit()

    keys_list = list(src_data_list[0].keys())
    if src_column not in keys_list:
        print(f'{src_file}源文件无{src_column}特征，请重试！')
        sys.exit()

    keys_list = list(judge_data_list[0].keys())
    if judge_colum not in keys_list:
        print(f'{judge_file}转换文件无{judge_colum}特征，请重试！')
        sys.exit()

    for t_col in translate_columns:
        if t_col not in keys_list:
            print(f'{judge_file}转换文件无{t_col}特征，请重试！')
            sys.exit()

    result_dict_list = []
    result_dict_list_un = []
    if only_one is False:
        for cur_index in range(0, len(src_data_list)):
            cur_column_arr = str(src_data_list[cur_index][src_column]).split("、")
            for cur_src_data in cur_column_arr:
                dict_v = {'ID': cur_index, judge_colum: cur_src_data}
                filtered_df = judge_df[judge_df[judge_colum] == cur_src_data]
                if filtered_df.shape[0] != 1:
                    print(f"{cur_src_data}在转换文件中存在{filtered_df.shape[0]}项，请注意!")
                    result_dict_list_un.append(dict_v)
                    continue
                for t_col in translate_columns:
                    dict_v[t_col] = filtered_df.iloc[0][t_col]
                result_dict_list.append(dict_v)

    if only_one is True:
        for cur_index in range(0, len(src_data_list)):
            cur_column_arr = str(src_data_list[cur_index][src_column]).split("、")
            dict_v = src_data_list[cur_index]
            # dict_v = {'ID': cur_index, judge_colum: src_data_list[cur_index][src_column]}
            for t_col in translate_columns:
                dict_v[f'{t_col}2'] = []

            for cur_src_data in cur_column_arr:
                filtered_df = judge_df[judge_df[judge_colum] == cur_src_data]
                un_legal = True
                if filtered_df.shape[0] != 1:
                    print(f"{cur_src_data}在转换文件中存在{filtered_df.shape[0]}项，请注意!")
                    dict_v_2 = {'ID': cur_index, judge_colum: cur_src_data}
                    result_dict_list_un.append(dict_v_2)
                else:
                    un_legal = False

                if filtered_df.shape[0] > 0:
                    for t_col in translate_columns:
                        dict_v[f'{t_col}2'] += str(filtered_df.iloc[0][t_col]).split("、")

            for t_col in translate_columns:
                dict_v[f'{t_col}T'] = "、".join(list(set(dict_v[f'{t_col}2'])))
                del dict_v[f'{t_col}2']
            result_dict_list.append(dict_v)

    save_dict_list_to_excel(result_dict_list, dst_file)


def translate_feature_v2(src_file,dst_file = 'Step2.四气、五味、归经、治法属性转换.xlsx'):
    src_column1 = '处方S'
    judge_colum1 = '品名'
    translate_columns1 = ['四气', '五味', '归经', '治法']
    compare_file_path = 'db/中药标准库V1.0.xlsx'
    translate_feature( src_file, dst_file,src_column1, judge_colum1, translate_columns1,compare_file_path,  False)

if __name__ == '__main__':
    translate_feature_v2('Step1.药物标准化后.xlsx')

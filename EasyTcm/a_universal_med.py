from a_med_stand import read_excel_to_dict_list, save_dict_list_to_excel
import os
import sys


def get_self_stand_name(src_col, mingcheng, bie_ming_src_list):
    for bieming in bie_ming_src_list:
        if mingcheng == bieming[src_col]:
            return bieming[src_col]
        if mingcheng in str(bieming['别名']).split("、"):
            return bieming[src_col]

    return None


def self_stand(col_name, compare_col_name, src_file, dst_stand_file, compare_file):
    """

    :param compare_col_name:
    :param col_name:
    :param src_file:
    :param dst_stand_file:
    :param compare_file:
    """
    unique_item_list = []

    bie_ming_dict_list = []
    self_dict_list = read_excel_to_dict_list(src_file)
    if len(self_dict_list) == 0:
        print(f'源文件无数据，程序已退出！({src_file})')
        sys.exit()

    keys_list = list(self_dict_list[0].keys())

    if col_name not in keys_list:
        print(f"源文件无{col_name}列,程序已退出！")
        sys.exit()

    for self_dict in self_dict_list:
        zheng_xing_list = str(self_dict[col_name]).split("、")
        if str(self_dict[col_name]) == 'nan':
            zheng_xing_list = []
        for zheng_xing in zheng_xing_list:
            if zheng_xing not in unique_item_list:
                unique_item_list.append(zheng_xing)

    for uil in unique_item_list:
        bie_ming_dict_list.append({col_name: uil, '别名': uil})

    if not os.path.exists(compare_file):
        save_dict_list_to_excel(bie_ming_dict_list, compare_file)

    bie_ming_dict_list = read_excel_to_dict_list(compare_file)
    self_dict_list = read_excel_to_dict_list(src_file)

    if len(self_dict_list) == 0:
        print(f'源文件无数据，程序已退出！({src_file})')
        sys.exit()

    keys_list = list(self_dict_list[0].keys())

    if col_name not in keys_list:
        print(f"源文件无{col_name}列,程序已退出！")
        sys.exit()

    if len(bie_ming_dict_list) == 0:
        print('特征规范标准库无数据,无法标准化')
        sys.exit()

    keys_list = list(bie_ming_dict_list[0].keys())

    if '别名' not in keys_list:
        print(f"特征规范标准库不包含别名列,无法标准化", os.path.abspath(compare_file), keys_list)
        sys.exit()

    if compare_col_name not in keys_list:
        print(f"特征规范标准库不包含{compare_col_name}列,无法标准化")
        sys.exit()

    for self_dict in self_dict_list:
        cur_items = str(self_dict[col_name]).replace("，", "、").replace("。", "、").split("、")
        dst_items = []
        un_dst_items = []
        if str(self_dict[col_name]) == 'nan':
            cur_items = []
        for cur_item in cur_items:
            stand_name = get_self_stand_name(compare_col_name, cur_item, bie_ming_dict_list)
            if stand_name is None:
                un_dst_items.append(cur_item)
            else:
                dst_items.append(stand_name)
        cur_index = self_dict_list.index(self_dict)
        self_dict_list[cur_index][f'{col_name}S'] = "、".join(dst_items)
        self_dict_list[cur_index][f'{col_name}U'] = "、".join(un_dst_items)
        self_dict_list[cur_index][f'{col_name}SU'] = "、".join(dst_items + un_dst_items)

    save_dict_list_to_excel(self_dict_list, dst_stand_file)


if __name__ == '__main__':
    src_col_name = '中医功效'
    compare_col_name ='治法'
    src_file_path = 'Step1.药物标准化后.xlsx'
    dst_file_path = src_file_path.replace('.xlsx',f'_{src_col_name}标准化.xlsx')
    compare_file_path = f'db/治法.xlsx'
    self_stand(src_col_name, compare_col_name,src_file_path, dst_file_path, compare_file_path)

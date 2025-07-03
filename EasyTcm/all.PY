import os

import zipfile

import os


def count_files_in_directory(directory_path):
    try:
        # 列出目录下所有文件和子目录，并过滤出文件
        only_files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        return len(only_files)
    except FileNotFoundError:
        print(f"目录 {directory_path} 不存在")
        return 0
    except PermissionError:
        print(f"没有权限访问目录 {directory_path}")
        return 0
    except Exception as e:
        print(f"发生错误: {e}")
        return 0


def zip_dir(directory, output_filename):
    # 创建一个ZipFile对象，并设置压缩模式为ZIP_DEFLATED
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历指定目录下的所有文件
        for root, dirs, files in os.walk(directory):
            for file in files:
                # 构建完整的路径，并添加到ZIP文件中
                filepath = os.path.join(root, file)
                # 使用arcname参数来避免在ZIP文件中包含完整的路径信息
                arcname = os.path.relpath(filepath, start=os.path.dirname(directory))
                zipf.write(filepath, arcname=arcname)


def split_path_os(filepath):
    # 将路径转为绝对路径
    abs_filepath = os.path.abspath(filepath)
    # 分离文件路径和文件名
    path, filename = os.path.split(abs_filepath)
    return path, filename


def move_xlsx_to_result_folder(src_folder='.', dst_folder='result'):
    import shutil

    """
    将源文件夹中的所有.xlsx文件移动到目标文件夹。

    参数:
        src_folder (str): 源文件夹路径，默认为当前文件夹 ('.')。
        dst_folder (str): 目标文件夹路径，默认为 'result'。
    """
    # 确保目标文件夹存在，如果不存在则创建
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
        print(f"创建了新的文件夹: {dst_folder}")

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(src_folder):
        # 检查文件是否为.xlsx文件
        if filename.endswith('.xlsx') or filename.endswith('.png') or filename.endswith('.svg'):
            src_file = os.path.join(src_folder, filename)
            dst_file = os.path.join(dst_folder, filename)

            # 如果目标文件已存在，则避免覆盖，可以添加编号或其他方式处理
            if os.path.exists(dst_file):
                base, ext = os.path.splitext(filename)
                counter = 1
                while os.path.exists(os.path.join(dst_folder, f"{base}_{counter}{ext}")):
                    counter += 1
                dst_file = os.path.join(dst_folder, f"{base}_{counter}{ext}")
                print(f"目标文件已存在，重命名为: {os.path.basename(dst_file)}")

            # 移动文件
            shutil.move(src_file, dst_file)
            print(f"已移动文件: {filename} 到 {dst_folder}")


import os


def modify_file_name(directory='', prefix='step2.四气、五味、归经、治法属性转换_', replace_prefix='step4.统计矩阵'):
    # 获取目录下的所有条目
    entries = os.listdir(directory)
    # 过滤出只包含文件并且文件名以指定前缀开头的列表
    files = [entry for entry in entries if os.path.isfile(os.path.join(directory, entry)) and entry.startswith(prefix)]

    for file_name in files:
        new_file_name = file_name.replace(prefix, replace_prefix, 1)  # 确保只替换最前面的一个匹配
        old_path = os.path.join(directory, file_name)
        new_path = os.path.join(directory, new_file_name)

        # 如果新文件名已存在，则先删除它
        if os.path.exists(new_path):
            os.remove(new_path)

        # 重命名文件
        os.rename(old_path, new_path)

    return files  # 返回被重命名的文件列表

import os

import pandas as pd
import sys
from tqdm import tqdm


def read_excel_to_dict_list(file_path):
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)

        # 将DataFrame转换为字典列表
        data_dict_list = df.to_dict(orient='records')

        return data_dict_list
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return None


def save_dict_list_to_excel(dict_list, excel_file_path, sheet_name='Sheet1'):
    """
    将字典列表转换为 Pandas DataFrame 并保存到 Excel 文件

    参数：
    - dict_list: 包含字典的列表
    - excel_file_path: Excel 文件保存路径
    - sheet_name: Excel 工作表名称，默认为 'Sheet1'
    """

    try:
        # 将字典列表转换为 Pandas DataFrame
        df = pd.DataFrame(dict_list)
        # 保存 DataFrame 到 Excel 文件
        df.to_excel(excel_file_path, sheet_name=sheet_name, index=False)
        print(f'saved DataFrame to Excel file: {excel_file_path}')

    except Exception as e:
        print(f"Error saving DataFrame to Excel file: {e}")
        return None


def contains_chinese_punctuation(text):
    chinese_punctuation_set = set('，。　！？；：‘’“”（）【】—《》…·「」『』﹃﹄〈〉﹁﹂【】〔〕—～·￥％＃＠＆＊＋－＝／｜＜＞〖〗◆■▲●★☆◎○→←↑↓—～…℃')
    for char in text:
        if char in chinese_punctuation_set:
            return True
    return False


def contains_punctuation(text):
    punctuation_set = set(
        '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~1234567890abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')
    for char in text:
        if char in punctuation_set:
            return True
    return False


def remove_punctuation(text):
    chinese_punctuation_set = set('，。！？；：‘’“”（）【】—《》…·「」『　』﹃﹄〈〉﹁﹂【】〔〕—～·￥％＃＠＆＊＋－＝／｜＜＞〖〗◆■▲●★☆◎○→←↑↓—～…℃')
    punctuation_set = set(
        '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~1234567890abcdefghi gklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\n')
    dst_text = ''
    for char in text:
        if char in punctuation_set or char in chinese_punctuation_set:
            pass
        else:
            dst_text += char
    return dst_text


def get_self_stand_name(mingcheng, bie_ming_src_list):
    if len(mingcheng) == 0:
        return None
    for bieming in bie_ming_src_list:
        if mingcheng == bieming['品名']:
            return bieming['药材名']

        if mingcheng == bieming['药材名']:
            return bieming['药材名']

        if mingcheng in str(bieming['别名']).split("、"):
            return bieming['药材名']

    for bieming in bie_ming_src_list:
        if mingcheng in str(bieming['物种名']).split("、"):
            return bieming['药材名']

    return None


def split_string_at_first_digit(input_str):
    num_index = None
    dig_list = '１２３４５６７８９０（('

    # 遍历字符串找到第一个数字出现的位置
    for i, char in enumerate(input_str):
        if char.isdigit() or char in dig_list:
            num_index = i
            break

    # 如果找到了数字，则分割字符串
    if num_index is not None:
        before_num = input_str[:num_index]
        return before_num
    else:
        return input_str


def get_stand_name(mingcheng, bie_ming_src_list):
    mingcheng = split_string_at_first_digit(mingcheng)
    mingcheng = remove_punctuation(mingcheng)
    zzfs = ['炒', '焦', '灸', '生', '鲜', '干', '炮', '烫', '锻', '炙', '煨', '制', '清', '法', '去土', '净', '去节',
            '煅', '陈', '燀', '杵',
            '去毛', '姜', '研末', '炭', '霜',
            '酒', '蜜', '盐', '醋',
            '云', '淮', '川', '广', '怀', '杭', '亳', '霍', '霍', '潞', '潼', '辽',
            '酒炙', '酒蒸', '麸炒', '炒焦', '盐炒', '酒炒', '盐水炒', '土炒',
            '或', '及', '与', '和', '等', '加', '各', '用量至', '组方', '组成', '用量', '药用', '剂量',
            '粉', '末', '片', '珠', '沫', '丝', '胶',
            '烊化', '先下', '先入', '先煎', '包', '包煎', '后下', '后入', '后煎', '去浮沫', '另冲', '冲服', '冲',
            '布包煎', '布包', '去皮', '去皮尖',
            '苷', '多糖', '嗪', '酸', '皂苷', '黄酮', '素', '总蒽醌', '嗪']
    sorted_zzfs = sorted(zzfs, key=len, reverse=True)
    dan_wei_list = []
    dw_list = ['两', '分', '斤', '枚', '斗', '升', 'g', 'G', '克', '份']
    sl_list = (('十一、十二、十三、十四、十五、十六、十七、十八、十九、一、二、三、四、五、六、七、八、九、十、半、两、'
                '10、11、12、13、14、15、16、17、18、19、20、25、30、40、50、60、70、80、90、100、'
                '0.1、0.2、0.3、0.4、0.6、0.5、0.9、1、2、3、4、5、6、7、8、9、'
                '１０、１１、１２、１３、１４、１５、１６、１７、１８、１９、２０、２５、３０、４０、５０、６０、７０、８０、９０、１００、'
                '０．１、０．２、０．３、０．４、０．５、０．６、０．９、１、２、３、５、６、４、７、８、９')
               .split("、"))
    for sl in sl_list:
        for dw in dw_list:
            dan_wei_list.append(sl + dw)
    for dan_wei in dan_wei_list:
        mingcheng = mingcheng.replace(dan_wei, '')
    result_md = get_self_stand_name(mingcheng, bie_ming_src_list)

    if result_md is None:
        for zz in zzfs:
            mingcheng = f'{zz}{mingcheng}'
            result_md = get_self_stand_name(mingcheng, bie_ming_src_list)
            if result_md is not None:
                return result_md
            mingcheng = f'{mingcheng}{zz}'
            result_md = get_self_stand_name(mingcheng, bie_ming_src_list)
            if result_md is not None:
                return result_md

    if result_md is None:
        for zz in sorted_zzfs:
            mingcheng = mingcheng.replace(zz, '')
            result_md = get_self_stand_name(mingcheng, bie_ming_src_list)
            if result_md is not None:
                return result_md

    return result_md


def medicine_stand(src_file, dst_stand_file, col_name='处方', compare_file='db/中药标准库V1.0.xlsx', min_num=-1, max_num=-1):
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
        print(f"特征规范标准库不包含别名列,无法标准化")
        sys.exit()

    if '药材名' not in keys_list:
        print(f"特征规范标准库不包含品名列,无法标准化")
        sys.exit()
    if '物种名' not in keys_list:
        print(f"特征规范标准库不包含品名列,无法标准化")
        sys.exit()
    if '品名' not in keys_list:
        print(f"特征规范标准库不包含品名列,无法标准化")
        sys.exit()

    for self_dict in tqdm(self_dict_list):
        cur_items = (str(self_dict[col_name])
                     .replace("天麦冬", "天冬、麦冬")
                     .replace("赤白芍", "赤芍、白芍")
                     .replace("赤白苓", "茯苓")
                     .replace(' ', '')
                     .replace('g', '、')
                     .replace(',', '、')
                     .replace('，', '、')
                     .replace('。', '、')
                     .replace('、、', '、')

                     .split("、"))
        dst_items = []
        un_dst_items = []
        if str(self_dict[col_name]) == 'nan':
            cur_items = []
        for cur_item in cur_items:
            stand_name = get_stand_name(cur_item, bie_ming_dict_list)
            if stand_name is None:
                un_dst_items.append(cur_item)
            else:
                dst_items.append(stand_name)
        cur_index = self_dict_list.index(self_dict)
        unique_items = sorted(list(set(dst_items)))

        self_dict_list[cur_index][f'{col_name}S'] = "、".join(unique_items)
        self_dict_list[cur_index][f'{col_name}SN'] = len(dst_items)
        self_dict_list[cur_index][f'{col_name}U'] = "、".join(un_dst_items)
        self_dict_list[cur_index][f'{col_name}SU'] = "、".join(dst_items + un_dst_items)

    if 0 < min_num < max_num:
        dst_dict_list = []
        for dict_v in self_dict_list:
            if min_num <= dict_v[f'{col_name}SN'] <= max_num:
                dst_dict_list.append(dict_v)
        save_dict_list_to_excel(dst_dict_list, dst_stand_file)
    else:
        save_dict_list_to_excel(self_dict_list, dst_stand_file)

    print(f'{dst_stand_file}列处理标准化完成')


if __name__ == '__main__':
    src_col_name = '处方'  # 要求输入，若未输入，默认值为处方
    src_file_path = 'data/test.xlsx'  # 要求上传或选择
    dst_file_path = src_file_path.replace('.xlsx', '_中药标准化.xlsx')  # 输出文件
    compare_file_path = 'db/中药标准库V1.0.xlsx'  # 要求上传
    min_med = 3
    max_med = 15
    medicine_stand(src_file_path, dst_file_path, src_col_name,compare_file_path, min_num=min_med, max_num=max_med)


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

from collections import defaultdict, Counter
from itertools import combinations



def generate_next_candidates(frequent_itemsets_by_size, k):
    """从频繁 (k-1) 项集中生成 k 项集候选"""
    candidates = []
    for i in range(len(frequent_itemsets_by_size[k - 2])):
        for j in range(i + 1, len(frequent_itemsets_by_size[k - 2])):
            # 前 k-2 项相同，最后一项不同的 (k-1) 项集可以合并成 k 项集
            itemset_i = list(frequent_itemsets_by_size[k - 2].keys())[i]
            itemset_j = list(frequent_itemsets_by_size[k - 2].keys())[j]
            if itemset_i[:k - 2] == itemset_j[:k - 2]:
                candidate = sorted(list(set(itemset_i) | set(itemset_j)))
                # 检查所有 (k-1) 子集是否都是频繁的
                if all(tuple(subset) in frequent_itemsets_by_size[k - 2] for subset in combinations(candidate, k - 1)):
                    candidates.append(candidate)
    return candidates


def find_frequent_itemsets(transactions, min_support):
    # 计算单项的支持度
    item_counts = Counter(item for transaction in transactions for item in transaction)
    frequent_items = {tuple([item]): count for item, count in item_counts.items() if
                      count / len(transactions) >= min_support}

    # 初始化频繁项集列表
    frequent_itemsets_by_size = [frequent_items]

    k = 2
    while True:
        # 生成下一层的候选项集
        candidates = generate_next_candidates(frequent_itemsets_by_size, k)

        # 如果没有新的候选项集，结束
        if not candidates:
            break

        # 计算候选项集的支持度
        candidate_counts = Counter()
        for transaction in transactions:
            for candidate in candidates:
                if all(item in transaction for item in candidate):
                    candidate_counts[tuple(candidate)] += 1

        # 筛选出频繁项集
        frequent_itemsets = {itemset: count for itemset, count in candidate_counts.items() if
                             count / len(transactions) >= min_support}

        if not frequent_itemsets:
            break

        frequent_itemsets_by_size.append(frequent_itemsets)
        k += 1

    # 合并所有大小的频繁项集
    all_frequent_itemsets = {itemset: count for layer in frequent_itemsets_by_size for itemset, count in layer.items()}

    return all_frequent_itemsets


def calculate_metrics(frequent_itemsets, transactions):
    num_transactions = len(transactions)
    rules = []

    for itemset, support_count in frequent_itemsets.items():
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                consequent = tuple(sorted(set(itemset) - set(antecedent)))
                antecedent_count = frequent_itemsets.get(tuple(antecedent), 0)
                consequent_count = frequent_itemsets.get(consequent, 0)

                if antecedent_count > 0 and consequent_count > 0:
                    confidence = support_count / antecedent_count
                    lift = confidence / (consequent_count / num_transactions)
                    rule = {
                        'antecedent': antecedent,
                        'consequent': consequent,
                        'support': support_count / num_transactions,
                        'confidence': confidence,
                        'lift': lift
                    }
                    rules.append(rule)
    return rules

def calculate_rulues(src_files, fre_file_path='frequent_itemsets.xlsx',rules_file_path='rules.xlsx',col_names='处方S',min_support=0.8,min_confidence=0.8,min_lift=1):
    from a_med_stand import save_dict_list_to_excel,read_excel_to_dict_list
    transactions=[]
    dict_list = read_excel_to_dict_list(src_files)
    for dict_item in dict_list:
        dict_item_list = dict_item[col_names].split("、")
        transactions.append(dict_item_list)

    frequent_items =[]
    frequent_itemsets = find_frequent_itemsets(transactions, min_support)
    for key in frequent_itemsets.keys():
        dict_item = {}
        dict_item['项集'] = "、".join(list(key))
        dict_item['支持度'] = frequent_itemsets[key]
        if dict_item['项集'].count("、")>0:
            frequent_items.append(dict_item)
    save_dict_list_to_excel(frequent_items, fre_file_path)

    # 计算关联规则的指标
    rules = calculate_metrics(frequent_itemsets, transactions)

    dst_rules = []
    dst_rules_for_draw = []
    # 打印结果
    for rule in rules:
        dict_rule = {}
        dict_rule['前项'] = "、".join(list(rule['antecedent']))
        dict_rule['后项'] = "、".join(list(rule['consequent']))
        dict_rule['支持度百分比'] = round(rule['support'], 4)*100
        dict_rule['置信度百分比'] = round(rule['confidence'], 2)*100
        dict_rule['提升度'] = round(rule['lift'], 4)*100
        if dict_rule['置信度百分比'] > min_confidence*100 and dict_rule['提升度'] > min_lift:
            dst_rules.append(dict_rule)
            if dict_rule['前项'].count("、")==0 and dict_rule['后项'].count("、")==0:
                dst_rules_for_draw.append(dict_rule)
            print(dict_rule)
    save_dict_list_to_excel(dst_rules, rules_file_path)
    rules_file_path_for_draw = rules_file_path.replace(".xlsx", "_for_draw.xlsx")
    save_dict_list_to_excel(dst_rules_for_draw, rules_file_path_for_draw)


if __name__ == '__main__':

    calculate_rulues('step1.药物标准化后.xlsx',min_support=0.1,min_confidence=0.8,min_lift=1)

from a_med_stand import read_excel_to_dict_list,save_dict_list_to_excel

def connect_columns(file_path,column_name1,column_name2,new_column_name,new_file_path):
    # read excel file to a dictionary list
    data_dict_list = read_excel_to_dict_list(file_path)

    # connect two columns and create a new column
    for data_dict in data_dict_list:
        if str(data_dict[column_name1]) == 'nan':
            data_dict[new_column_name] = data_dict[column_name2]
        if str(data_dict[column_name2]) == 'nan':
            data_dict[new_column_name] = data_dict[column_name1]
        if str(data_dict[column_name1])!= 'nan' and str(data_dict[column_name2])!= 'nan':
            data_dict[new_column_name] = data_dict[column_name1] + data_dict[column_name2]
        if str(data_dict[column_name1]) == 'nan' and str(data_dict[column_name2]) == 'nan':
            data_dict[new_column_name] = ''

    # save the updated dictionary list to a new excel file
    save_dict_list_to_excel(data_dict_list,new_file_path)

if __name__ == '__main__':
    a = []
    b = ['b1','b2','b3']
    c = a + b
    print(c)

    from a_med_stand import read_excel_to_dict_list, save_dict_list_to_excel


def connect_rect(rect1_file, rect2_file, dst_file):
    rect_list = read_excel_to_dict_list(rect1_file)
    rect2_list = read_excel_to_dict_list(rect2_file)
    dst = []
    for idx in range(len(rect_list)):
        rect1 = rect_list[idx]
        rect2 = rect2_list[idx]
        dict_v = {}
        for key in rect1.keys():
            dict_v[key] = rect1[key]
        for key in rect2.keys():
            dict_v[key] = rect2[key]
        dst.append(dict_v)
    save_dict_list_to_excel(dst, dst_file)


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

import pandas as pd
from scipy.stats import fisher_exact
import numpy as np
import seaborn as sns
from pypinyin import pinyin, Style

# 将中文转换为拼音
def chinese_to_pinyin(chinese_text):
    pinyin_text = pinyin(chinese_text, style=Style.NORMAL)
    return ''.join([word[0].capitalize() for word in pinyin_text])  # 提取拼音的首字母并连接成字符串

def fisher(file_path, png_file, dst_file='', cmap='viridis'):
    import matplotlib

    matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
    import matplotlib.pyplot as plt
    # 使用pandas读取Excel文件
    df = pd.read_excel(file_path)
    # 获取列名列表，并将列名转换为拼音
    columns = df.columns.tolist()
    columns_pinyin = [chinese_to_pinyin(col) for col in columns]  # 列名转换为拼音
    # 存储结果的字典
    results = {}

    # 对于每一对列
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            # 提取两个列的数据并转换为2x2列联表形式
            table = pd.crosstab(df[columns[i]], df[columns[j]])

            try:
                # 进行Fisher精确检验
                oddsratio, p_value = fisher_exact(table)

                # 计算共现率
                co_occurrence_rate = table.loc[1, 1] / table.sum().sum()

                results[(columns[i], columns[j])] = {
                    'oddsratio': oddsratio,
                    'p-value': p_value,
                    'co-occurrence_rate': co_occurrence_rate
                }
            except ValueError as e:
                # 如果数据不适合进行Fisher精确检验，则记录错误信息
                results[(columns[i], columns[j])] = {'error': str(e)}

    # 创建DataFrame来存储共现率，指定数据类型为浮点型
    co_occurrence_df = pd.DataFrame(index=columns_pinyin, columns=columns_pinyin, dtype=float).fillna(0)
    # 创建一个DataFrame来存储p值
    p_values_df = pd.DataFrame(index=columns_pinyin, columns=columns_pinyin, dtype=float).fillna(1)  # 默认填充为1，表示不显著

    # 填充共现率和p值的DataFrame
    for (col1, col2), result in results.items():
        co_occurrence_df.at[chinese_to_pinyin(col1), chinese_to_pinyin(col2)] = result['co-occurrence_rate']
        p_values_df.at[chinese_to_pinyin(col1), chinese_to_pinyin(col2)] = result['p-value']

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

    # 创建一个掩码，用于隐藏下半部分以及值为0的部分
    mask = np.tril(np.ones_like(co_occurrence_df, dtype=bool))

    # 绘制热图
    plt.figure(figsize=(16, 12))
    ax = sns.heatmap(co_occurrence_df, annot=True, cmap=cmap, mask=mask, fmt='.2f')

    # 遍历p_values_df，找到所有p-value < 0.05的单元格并在热图上标记
    significant_pairs = []
    for i in range(len(columns_pinyin)):
        for j in range(i + 1, len(columns_pinyin)):
            if p_values_df.iloc[i, j] < 0.05:
                # 在热图对应位置添加红色实心圆
                ax.plot(j + 0.5, i + 0.8, 'ro', markersize=7, markeredgewidth=0)
                # 收集显著性组合
                significant_pairs.append({
                    'Column 1': columns_pinyin[i],
                    'Column 2': columns_pinyin[j],
                    'Odds Ratio': round(results[(columns[i], columns[j])]['oddsratio'], 4),
                    'P-value': round(results[(columns[i], columns[j])]['p-value'], 4),
                    'Co-occurrence Rate': round(results[(columns[i], columns[j])]['co-occurrence_rate'], 4)
                })

    # 调整x轴的位置到顶部
    # 设置 y 轴标签为水平方向
    for tick in ax.yaxis.get_ticklabels():
        tick.set_rotation(0)
    plt.gca().xaxis.set_ticks_position('top')
    plt.gca().xaxis.set_label_position('top')

    # 显示标题（可选）
    # plt.title('Co-occurrence Rate Heatmap with Significant P-values Marked')

    plt.savefig(png_file, dpi=300, bbox_inches='tight')

    # 将显著性组合写入文件
    if dst_file:
        # 将显著性组合转换为DataFrame
        significant_df = pd.DataFrame(significant_pairs)
        # 写入Excel文件
        significant_df.to_excel(dst_file, index=False)
        print(f"Significant pairs have been written to {dst_file}")

# 示例调用
if __name__ == '__main__':
    src_file = r'D:\成果转化\数据挖掘\樱桃小丸子明\dst\定稿\9_高频关联矩阵_处方S_10矩阵.xlsx'
    dst_file = r'显著性药对.xlsx'  # 指定输出文件路径
    fisher(src_file, '显著性药对检验.png', dst_file=dst_file)

import matplotlib
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
from a_med_stand import save_dict_list_to_excel
from pypinyin import lazy_pinyin  # 导入拼音库

matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


def convert_to_pinyin(text):
    """将中文转换为拼音"""
    return ''.join([p.capitalize() for p in lazy_pinyin(text)])


def class_z(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 转置数据框以便对变量进行聚类
    transposed_df = df.T

    # 计算层次聚类
    Z = linkage(transposed_df, 'ward')

    # 提取所有节点间的距离，并去重
    distances = list(np.unique(Z[:, 2]))
    availuable = []
    for d in distances[1:]:
        d1 = distances[distances.index(d) - 1]
        availuable.append(round((d + d1) / 2, 2))

    return Z, transposed_df, availuable


def class_z2(file_path, line_dis, number, dst_png_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 转置数据框以便对变量进行聚类
    transposed_df = df.T

    # 计算层次聚类
    Z = linkage(transposed_df, 'ward')  # 使用ward方法
    base_count = len(transposed_df)

    # 获取列名作为标签
    labels = transposed_df.index.tolist()

    # 将标签转换为拼音
    labels_pinyin = [convert_to_pinyin(label) for label in labels]

    # 绘制水平方向的树状图
    plt.figure(figsize=(10, 7))
    dendro = dendrogram(Z, labels=labels_pinyin, orientation='right', leaf_font_size=8)
    plt.xlabel('Distance')
    plt.ylabel('Variable')

    # 获取y轴的范围
    y_lim = plt.ylim()

    # 查找距离为line_dis的位置并绘制垂直线
    distances = Z[:, 2]
    closest_distance_index = np.argmin(np.abs(distances - line_dis))
    closest_distance = distances[closest_distance_index]

    # 查找比最接近距离更小的下一个距离
    lower_distance = None
    upper_distance = None
    if closest_distance > line_dis:
        lower_distance = distances[np.max(np.where(distances < closest_distance))]
        upper_distance = closest_distance
    elif closest_distance < line_dis:
        upper_distance = distances[np.min(np.where(distances > closest_distance))]
        lower_distance = closest_distance
    else:
        # 如果最接近的距离正好等于line_dis，那么就绘制这条线
        idx = np.where(Z[:, 2] == closest_distance)[0][0]
        x = Z[idx, 2]
        plt.vlines(x=x, ymin=y_lim[0], ymax=y_lim[1], colors='r', linestyles='--', label=f'Distance {line_dis}')
        plt.legend()
        plt.savefig(f'{dst_png_path}_{number}.png')
        plt.close()
        return Z, transposed_df, [lower_distance, upper_distance]

    if lower_distance is not None and upper_distance is not None:
        # 在最接近的距离之间绘制竖线
        plt.vlines(x=(lower_distance + upper_distance) / 2, ymin=y_lim[0], ymax=y_lim[1],
                   colors='r', linestyles='--', label=f'Distance =  {line_dis}')
        plt.legend()

    plt.savefig(f'{dst_png_path}_{number}.png')
    plt.close()

    # 提取所有节点间的距离，并去重
    distances_unique = list(np.unique(Z[:, 2]))
    availuable = []
    for d in distances_unique[1:]:
        d1 = distances_unique[distances_unique.index(d) - 1]
        availuable.append(round((d + d1) / 2, 2))

    return Z, transposed_df, [lower_distance, upper_distance]


def get_number_of_clusters(Z, dis):
    from scipy.cluster.hierarchy import fcluster
    #
    flusters = fcluster(Z, dis, criterion='distance')
    unique_clusters = np.unique(flusters)
    return len(unique_clusters), flusters


def get_class_by_distance(distance_threshold, Z, transposed_df):
    num_clusters, cluster_assignment = get_number_of_clusters(Z, distance_threshold)

    # 创建一个新的 DataFrame 来存储簇分配信息
    cluster_df = pd.DataFrame({'Cluster': cluster_assignment, 'Variable': transposed_df.index})

    # 使用 groupby 方法来根据簇号对变量进行分组
    grouped = cluster_df.groupby('Cluster')

    class_dst = []
    max_count = 0
    min_count = 100
    # 输出每个簇中的变量
    for cluster_id, group in grouped:
        class_dst.append({'Cluster': cluster_id, 'values': group['Variable'].to_list()})
        if len(group['Variable'].values) > max_count:
            max_count = len(group['Variable'].values)

        if len(group['Variable'].values) < min_count:
            min_count = len(group['Variable'].values)

    return num_clusters, class_dst, max_count - min_count


# 使用示例


def class_z_final(file_path, dst_xls_path='step11_dst.xlsx', dst_png_path='cluster', mim_num_clusters=4,
                 max_num_clusters=8):
    Z, df, values = class_z(file_path)
    result = []
    for d in values:
        num_clusters, dst_class, de_count = get_class_by_distance(d, Z, df)
        if mim_num_clusters <= num_clusters <= max_num_clusters:
            for c in dst_class:
                dst_class[dst_class.index(c)]['num_clusters'] = num_clusters
                dst_class[dst_class.index(c)]['distance'] = d
                result.append(c)
            class_z2(file_path, d, num_clusters, dst_png_path)
    save_dict_list_to_excel(result, dst_xls_path)


if __name__ == '__main__':
    src_file_path = 'result/step8.高频药物矩阵10.xlsx'
    class_z_final(src_file_path)

import json
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
from upset import draw_up_set, find_frequent_itemsets
from a_med_stand import save_dict_list_to_excel
from pypinyin import pinyin, lazy_pinyin

def chinese_to_pinyin(text):
    # 将中文转换为拼音，并将每个拼音的首字母大写
    return ''.join([p.capitalize() for p in lazy_pinyin(text)])


def pca_analysis(file_path, output_xlsx='pca.xlsx', pca3d_png='pca3d.png', upset_png='upset.png', rat_png='rat.png', percentile=0.8):
    import pandas as pd
    # 读取 Excel 文件
    df = pd.read_excel(file_path)
    # 获取特征名称（第一行作为列名），并转换为拼音
    feature_names = [chinese_to_pinyin(name) for name in df.columns]
    # 获取数据部分（去掉第一行）
    X = df.values
    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # 创建 PCA 模型
    n_components = min(len(feature_names), len(feature_names))  # 至少需要3个主成分来绘制3D图
    pca = PCA(n_components=n_components)
    # 拟合模型并转换数据
    X_pca = pca.fit_transform(X_scaled)
    # 输出特征值（每个主成分的方差）
    print("Eigenvalues (Explained Variance):", pca.explained_variance_)
    # 输出方差百分比
    print("Variance Ratio (%):", pca.explained_variance_ratio_ * 100)
    # 计算累计方差百分比
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    print("Cumulative Variance (%):", cumulative_variance * 100)
    min_components = np.argmax(cumulative_variance >= percentile) + 1

    up_set_arr = []
    # 输出特征向量
    print("\nFeature vectors (components):")
    ven_arr = []
    component_arr = []
    for i, component in enumerate(pca.components_):
        if i < min_components:
            # 将特征向量转换为 Pandas Series，并按绝对值排序
            component_series = pd.Series(component, index=feature_names).abs().sort_values(ascending=False)

            # 输出绝对值最大的8项
            top_8_features = component_series.head(8)
            top_8_json = json.loads(top_8_features.to_json(force_ascii=False, indent=4))
            ven_arr.append(list(top_8_json.keys()))
            print(f"Component {i + 1}: {dict(component_series)}")
            component_arr.append(dict(component_series))
    save_dict_list_to_excel(component_arr, output_xlsx)
    # 将数据转换为 DataFrame
    df = pd.DataFrame({
        'features': ven_arr
    })
    print(df)

    # 查找累积解释方差大于等于80%所需的最小主成分数
    # 可视化 PCA 结果
    plt.figure(figsize=(8, 6))
    plt.bar(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_ * 100, alpha=0.5,
            align='center')
    plt.step(range(1, len(cumulative_variance) + 1), cumulative_variance * 100, where='mid',
             label='Cumulative Variance')
    plt.axhline(y=80, color='r', linestyle='--', label='80% Explained Variance')  # 添加水平线
    # 绘制垂直线
    plt.axvline(x=min_components, color='g', linestyle='--', label=f'Min Components for >=80% ({min_components})')

    plt.ylabel('Explained Variance (%)')
    plt.xlabel('Principal Component')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(rat_png, dpi=300)

    # 绘制3D载荷图
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    x_loadings = pca.components_[0]
    y_loadings = pca.components_[1]
    z_loadings = pca.components_[2]

    for i in range(len(x_loadings)):
        ax.text(x_loadings[i], y_loadings[i], z_loadings[i], feature_names[i], color="red")

    ax.scatter(x_loadings, y_loadings, z_loadings)
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    # plt.title('3D Loadings Plot')
    plt.savefig(pca3d_png, dpi=300)
    print(ven_arr)
    fre = find_frequent_itemsets(ven_arr)
    draw_up_set(ven_arr, upset_png)
    max = 1
    for f_ in fre:
        if f_['count'] > max:
            max = f_['count']
    for f_ in fre:
        if f_['count'] == max:
            print(f_)
    plt.close()

if __name__ == '__main__':
    pca_analysis('result/step8.高频药物矩阵10.xlsx')

import json
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
from upset import draw_up_set, find_frequent_itemsets
from a_med_stand import save_dict_list_to_excel
from pypinyin import pinyin, lazy_pinyin

def chinese_to_pinyin(text):
    # 将中文转换为拼音，并将每个拼音的首字母大写
    return ''.join([p.capitalize() for p in lazy_pinyin(text)])


def pca_analysis(file_path, output_xlsx='pca.xlsx', pca3d_png='pca3d.png', upset_png='upset.png', rat_png='rat.png', percentile=0.8):
    import pandas as pd
    # 读取 Excel 文件
    df = pd.read_excel(file_path)
    # 获取特征名称（第一行作为列名），并转换为拼音
    feature_names = [chinese_to_pinyin(name) for name in df.columns]
    # 获取数据部分（去掉第一行）
    X = df.values
    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # 创建 PCA 模型
    n_components = min(len(feature_names), len(feature_names))  # 至少需要3个主成分来绘制3D图
    pca = PCA(n_components=n_components)
    # 拟合模型并转换数据
    X_pca = pca.fit_transform(X_scaled)
    # 输出特征值（每个主成分的方差）
    print("Eigenvalues (Explained Variance):", pca.explained_variance_)
    # 输出方差百分比
    print("Variance Ratio (%):", pca.explained_variance_ratio_ * 100)
    # 计算累计方差百分比
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    print("Cumulative Variance (%):", cumulative_variance * 100)
    min_components = np.argmax(cumulative_variance >= percentile) + 1

    up_set_arr = []
    # 输出特征向量
    print("\nFeature vectors (components):")
    ven_arr = []
    component_arr = []
    for i, component in enumerate(pca.components_):
        if i < min_components:
            # 将特征向量转换为 Pandas Series，并按绝对值排序
            component_series = pd.Series(component, index=feature_names).abs().sort_values(ascending=False)

            # 输出绝对值最大的8项
            top_8_features = component_series.head(8)
            top_8_json = json.loads(top_8_features.to_json(force_ascii=False, indent=4))
            ven_arr.append(list(top_8_json.keys()))
            print(f"Component {i + 1}: {dict(component_series)}")
            component_arr.append(dict(component_series))
    save_dict_list_to_excel(component_arr, output_xlsx)
    # 将数据转换为 DataFrame
    df = pd.DataFrame({
        'features': ven_arr
    })
    print(df)

    # 查找累积解释方差大于等于80%所需的最小主成分数
    # 可视化 PCA 结果
    plt.figure(figsize=(8, 6))
    plt.bar(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_ * 100, alpha=0.5,
            align='center')
    plt.step(range(1, len(cumulative_variance) + 1), cumulative_variance * 100, where='mid',
             label='Cumulative Variance')
    plt.axhline(y=80, color='r', linestyle='--', label='80% Explained Variance')  # 添加水平线
    # 绘制垂直线
    plt.axvline(x=min_components, color='g', linestyle='--', label=f'Min Components for >=80% ({min_components})')

    plt.ylabel('Explained Variance (%)')
    plt.xlabel('Principal Component')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(rat_png, dpi=300)

    # 绘制3D载荷图
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    x_loadings = pca.components_[0]
    y_loadings = pca.components_[1]
    z_loadings = pca.components_[2]

    for i in range(len(x_loadings)):
        ax.text(x_loadings[i], y_loadings[i], z_loadings[i], feature_names[i], color="red")

    ax.scatter(x_loadings, y_loadings, z_loadings)
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    # plt.title('3D Loadings Plot')
    plt.savefig(pca3d_png, dpi=300)
    print(ven_arr)
    fre = find_frequent_itemsets(ven_arr)
    draw_up_set(ven_arr, upset_png)
    max = 1
    for f_ in fre:
        if f_['count'] > max:
            max = f_['count']
    for f_ in fre:
        if f_['count'] == max:
            print(f_)
    plt.close()

if __name__ == '__main__':
    pca_analysis('result/step8.高频药物矩阵10.xlsx')

import sys
import random
from pycirclize import Circos
import pandas as pd
from pypinyin import pinyin, Style  # 导入pypinyin库

# 设置Matplotlib支持中文


def generate_matrix(rows, cols):
    # 创建一个空的列表来存储矩阵
    matrix_data = []

    # 使用嵌套循环来生成矩阵
    for _ in range(rows):
        row = [0] * cols
        matrix_data.append(row)

    return matrix_data

def convert_to_pinyin(text):
    """ 将中文文本转换为拼音 """
    return ''.join([word[0].capitalize() for word in pinyin(text, style=Style.NORMAL)])

def get_data(file_path, min_sups=0, min_con=0, mod='支持度'):
    df = pd.read_excel(file_path)
    data_dict_list = df.to_dict(orient='records')
    row_names = []
    for r in data_dict_list:
        sup = float(r['支持度百分比'])
        con = float(r['置信度百分比'])
        if sup >= min_sups > 0 and con >= min_con > 0:
            row_ = r[list(r.keys())[0]]
            col_ = r[list(r.keys())[1]]
            # 将中文转换为拼音
            row_pinyin = convert_to_pinyin(row_)
            col_pinyin = convert_to_pinyin(col_)
            if row_pinyin not in row_names:
                row_names.append(row_pinyin)
            if col_pinyin not in row_names:
                row_names.append(col_pinyin)

    matrix_data = generate_matrix(len(row_names), len(row_names))
    for r in data_dict_list:
        row_ = r[list(r.keys())[0]]
        col_ = r[list(r.keys())[1]]
        sup = float(r['支持度百分比'])
        con = float(r['置信度百分比'])
        if sup >= min_sups > 0 and con >= min_con > 0:
            # 将中文转换为拼音
            row_pinyin = convert_to_pinyin(row_)
            col_pinyin = convert_to_pinyin(col_)
            idx_row = row_names.index(row_pinyin)
            idx_col = row_names.index(col_pinyin)
            if mod == '支持度':
                matrix_data[idx_row][idx_col] = sup
            if mod == '置信度':
                matrix_data[idx_row][idx_col] = con
    return matrix_data, row_names

def draw_rule(file_path, png_path, min_sup=1, min_con=1, mod='置信度'):
    import matplotlib
    matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
    import matplotlib.pyplot as plt

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体（可替换为其他拼音支持字体）
    plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    matrix_data, row_names = get_data(file_path, min_sup, min_con, mod)
    print(matrix_data)
    print(len(row_names))
    matrix_df = pd.DataFrame(matrix_data, index=row_names, columns=row_names)

    circos = Circos.initialize_from_matrix(
        matrix_df,
        start=-265,
        end=95,
        space=5,
        r_lim=(93, 100),
        cmap="tab10",
        label_kws=dict(r=94, size=8, color="white"),
        link_kws=dict(ec="black", lw=0.5),
    )

    # Plot the figure
    fig = circos.plotfig()
    # Save the figure to a file
    fig.savefig(png_path, dpi=300, bbox_inches='tight')
    # Optionally, show the figure
    # plt.show()

if __name__ == '__main__':
    file_path = "rules_for_draw.xlsx"  # 你的数据文件路径
    png_path = 'chord_diagram.png'  # 输出图片路径
    min_sup = 1  # 最小支持度
    min_con = 1  # 最小置信度
    mod = '置信度'  # 使用的指标，支持度或置信度
    draw_rule(file_path, png_path, min_sup, min_con, mod)

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
from pypinyin import pinyin, Style

# 将中文转换为拼音
def chinese_to_pinyin(chinese_text):
    pinyin_text = pinyin(chinese_text, style=Style.NORMAL)  # 转换为拼音
    return ''.join([word[0].capitalize() for word in pinyin_text])  # 提取拼音的首字母并连接成字符串

def generate_wordcloud(csv_file, save_path, width=800, height=400, dpi=300):
    # 读取CSV文件
    df = pd.read_csv(csv_file, encoding='utf-8')  # 如果CSV文件编码不是UTF-8，请修改为正确的编码格式
    num_colors = df.shape[0]
    # 提取元素和频次列
    elements = df.iloc[:, 0].tolist()
    frequencies = df.iloc[:, 1].tolist()

    # 将中文元素转换为拼音
    elements_pinyin = [chinese_to_pinyin(element) for element in elements]

    # 创建一个空字典来存储元素及其频次
    word_freq = {}
    for element, freq in zip(elements_pinyin, frequencies):  # 使用拼音作为键
        word_freq[element] = freq

    # 创建WordCloud对象，并配置参数
    # 设置字体为中文字体（例如微软雅黑）
    font_path = "C:/Windows/Fonts/msyh.ttc"  # 请替换为你系统上的中文字体文件路径

    # 生成一个随机颜色列表，用于设置词云图的颜色
    color_palette = list(plt.cm.tab20.colors)  # 将元组转换为列表
    np.random.shuffle(color_palette)
    color_map = ListedColormap(color_palette[:num_colors])

    wordcloud = WordCloud(width=width, height=height, background_color='white', font_path=font_path, colormap=color_map).generate_from_frequencies(word_freq)

    # 绘制词云图
    plt.figure(figsize=(width/100, height/100))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 关闭坐标轴

    # 保存词云图
    plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    plt.close()

def generate_wordcloud_from_xlsx(xlsx_file, save_path, width=800, height=400, dpi=300):
    # 读取Excel文件
    df = pd.read_excel(xlsx_file)  # 如果Excel文件编码不是UTF-8，请修改为正确的编码格式
    num_colors = df.shape[0]
    # 提取元素和频次列
    elements = df.iloc[:, 0].tolist()
    frequencies = df.iloc[:, 1].tolist()

    # 将中文元素转换为拼音
    elements_pinyin = [chinese_to_pinyin(element) for element in elements]

    # 创建一个空字典来存储元素及其频次
    word_freq = {}
    for element, freq in zip(elements_pinyin, frequencies):  # 使用拼音作为键
        word_freq[element] = freq

    # 创建WordCloud对象，并配置参数
    # 设置字体为中文字体（例如微软雅黑）
    font_path = "C:/Windows/Fonts/msyh.ttc"  # 请替换为你系统上的中文字体文件路径

    # 生成一个随机颜色列表，用于设置词云图的颜色
    color_palette = list(plt.cm.tab20.colors)  # 将元组转换为列表
    np.random.shuffle(color_palette)
    color_map = ListedColormap(color_palette[:num_colors])

    wordcloud = WordCloud(width=width, height=height, background_color='white', font_path=font_path, colormap=color_map).generate_from_frequencies(word_freq)

    # 绘制词云图
    plt.figure(figsize=(width/100, height/100))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 关闭坐标轴

    # 保存词云图
    plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    plt.close()

def generate_wordcloud_pic(csv_file, save_tag_path, times, width=1000, height=600, dpi=600):
    if csv_file.endswith('.xlsx'):
        for index in range(1, times + 1):
            save_path = f'{save_tag_path}_{index}.png'
            generate_wordcloud_from_xlsx(csv_file, save_path, width=width, height=height, dpi=dpi)
    else:
        for index in range(1, times + 1):
            save_path = f'{save_tag_path}_{index}.png'
            generate_wordcloud(csv_file, save_path, width=width, height=height, dpi=dpi)


# Example usage:

# csv_file = '无/肩周炎_8_dst_处方S_高频统计.csv'
# generate_wordcloud_pic(csv_file,'无/定稿/高频药物图',5)
#
# csv_file = '无/肩周炎_7_dst_穴位S_高频统计.csv'
# generate_wordcloud_pic(csv_file,'无/定稿/高频穴位图',5)
#
#
# csv_file = '无/肩周炎_6_dst_处方S_标准统计.csv'
# generate_wordcloud_pic(csv_file,'无/定稿/全部药物图',5)
#
# csv_file = '无/肩周炎_5_dst_穴位S_标准统计.csv'
# generate_wordcloud_pic(csv_file,'无/定稿/全部穴位图',5)



# src_folder = 'D:\数据挖掘实战\从虚论治失眠'
# dst_folder = f'{src_folder}/dst'
# generate_wordcloud_pic(f'{dst_folder}/定稿/5_统计_证型S_.xlsx',f'{dst_folder}/定稿/5_统计_证型S_词云图',5)

# Example usage:

# csv_file = '无/肩周炎_8_dst_处方S_高频统计.csv'
# generate_wordcloud_pic(csv_file,'无/定稿/高频药物图',5)
#
# csv_file = '无/肩周炎_7_dst_穴位S_高频统计.csv'
# generate_wordcloud_pic(csv_file,'无/定稿/高频穴位图',5)
#
#
# csv_file = '无/肩周炎_6_dst_处方S_标准统计.csv'
# generate_wordcloud_pic(csv_file,'无/定稿/全部药物图',5)
#
# csv_file = '无/肩周炎_5_dst_穴位S_标准统计.csv'
# generate_wordcloud_pic(csv_file,'无/定稿/全部穴位图',5)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import random
from pypinyin import pinyin, Style

# 将中文转换为拼音
def chinese_to_pinyin(chinese_text):
    pinyin_text = pinyin(chinese_text, style=Style.NORMAL)
    return ''.join([word[0].capitalize() for word in pinyin_text])  # 提取拼音的首字母并连接成字符串

def generate_radar_chart(csv_file, save_path_prefix, num_charts=5, width=1000, height=600, dpi=600, show_value=False):
    for i in range(num_charts):
        random_color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
        save_path = f'{save_path_prefix}{i+1}.png'
        generate_single_radar_chart(csv_file, save_path, color=random_color, width=width, height=height, dpi=dpi, show_value=show_value)
        print(i)

def generate_single_radar_chart(csv_file, save_path, color='skyblue', width=800, height=400, dpi=300, show_value=False):
    # 读取CSV文件
    if csv_file.endswith(".csv"):
        df = pd.read_csv(csv_file, encoding='utf-8')  # 如果CSV文件编码不是UTF-8，请修改为正确的编码格式
    else:
        df = pd.read_excel(csv_file)  # 如果CSV文件编码不是UTF-8，请修改为正确的编码格式

    # 提取元素和频次列
    elements = df.iloc[:, 0].tolist()
    frequencies = df.iloc[:, 1].tolist()

    # 将中文元素转换为拼音
    elements_pinyin = [chinese_to_pinyin(element) for element in elements]

    # 绘制雷达图
    categories = elements_pinyin  # 使用拼音作为标签
    values = frequencies

    # 添加第一个数据到最后，以闭合雷达图
    values += values[:1]

    # 计算角度
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    # 创建雷达图
    fig, ax = plt.subplots(figsize=(width/100, height/100), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color=color, alpha=0.5)
    ax.plot(angles, values, color=color, linewidth=2, linestyle='solid')
    ax.set_xticks(angles[:-1])

    # 添加数值标签
    if show_value:
        max_value = max(values)
        for angle, value in zip(angles, values):
            ax.text(angle, max_value, f'{value:d}', ha='center', va='center', fontsize=8)

    # 设置拼音标签（可以使用拼音字体来适配拼音字符）
    ax.set_xticklabels(categories, fontproperties=FontProperties(fname="C:/Windows/Fonts/msyh.ttc"))

    ax.set_yticklabels([])

    # 保存雷达图
    plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    print(save_path)
    plt.close()

if __name__ == '__main__':
    csv_file = 'D:\\成果转化\\数据挖掘\\DM_广中医\\13610215701内服\\dst\\定稿\\5_统计_归经_.xlsx'
    save_path_prefix = 'D:\\成果转化\\数据挖掘\\DM_广中医\\13610215701内服\\dst\\定稿\\5_统计_归经_'
    generate_radar_chart(csv_file, save_path_prefix, num_charts=5, width=1000, height=600, dpi=300, show_value=True)

#
# # Example usage:
# csv_file = '无/肩周炎_2_dst_五味_整体统计.csv'
# save_path_prefix = ''
# generate_radar_chart(csv_file, save_path_prefix, num_charts=5, width=1000, height=600, dpi=300)
#
# csv_file = '无/肩周炎_1_dst_归经_整体统计.csv'
# save_path_prefix = '无/定稿/归经图'
# generate_radar_chart(csv_file, save_path_prefix, num_charts=5, width=1000, height=600, dpi=300)
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
import random
from pypinyin import lazy_pinyin  # 导入拼音转换库

def read_csv_to_dict_list(file_path):
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            print("Unsupported file format. Only CSV and XLSX are supported.")
            return None
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def generate_transparent_colors1(color):
    r, g, b = [component / 255 for component in color]
    return [(r, g, b, index / 5 + 0.1) for index in range(5)]

def generate_transparent_colors2(color):
    r, g, b = [component / 255 for component in color]
    return [(r, g, b, 1 - index / 5 - 0.1) for index in range(5)]

def generat_pie_pic(ping_color, hot_color, cold_color, save_path, labels, sizes):
    plt.clf()
    plt.cla()
    plt.close()
    color_s = []
    ping_color_rgba = (ping_color[0] / 255, ping_color[1] / 255, ping_color[2] / 255, 0.5)
    color_s.append(ping_color_rgba)
    color_s += generate_transparent_colors2(hot_color)
    color_s += generate_transparent_colors1(cold_color)

    category2_index = labels.index('平')
    start_angle = -float(sizes[0]) / sum(sizes) * 180
    explode = [0 if i == category2_index else 0 for i in range(len(labels))]

    # 将 labels 转换为拼音
    labels_pinyin = [' '.join([word.capitalize() for word in lazy_pinyin(label)]) for label in labels]


    # 使用非中文字体
    font = FontProperties(fname=r"c:\windows\fonts\times.ttf", size=6)

    # 绘制饼图
    patches, texts, autotexts = plt.pie(
        sizes, explode=explode, colors=color_s, autopct='%1.2f%%', shadow=False,
        startangle=start_angle, textprops={'fontproperties': font}, rotatelabels=False
    )

    plt.axhline(y=0, color='black', linestyle='--', linewidth=2)

    # 修改图例为拼音
    plt.legend(patches, [f"{l}, {s / sum(sizes) * 100:.2f} %" for l, s in zip(labels_pinyin, sizes)],
               loc='lower right', fontsize=8, prop=font)

    for autotext in autotexts:
        autotext.set_visible(False)

    plt.axis('equal')
    plt.savefig(save_path, dpi=600)
    plt.close()

def generat_pie_sqt(sq_file, save_path):
    labels = ['平', '大热', '热', '微热', '温', '微温', '微凉', '凉', '微寒', '寒', '大寒']
    sizes = [0] * len(labels)
    dict_list = read_csv_to_dict_list(sq_file)

    for si in labels:
        index = labels.index(si)
        for sq in dict_list:
            if sq['Item3'] == labels[index]:
                sizes[index] = sq['times']

    light_blue_rgb1 = (0, 191, 255)
    hot_color = (255, 0, 0)
    cold_color = (0, 255, 0)
    generat_pie_pic(light_blue_rgb1, hot_color, cold_color, save_path, labels, sizes)

if __name__ == '__main__':
    generat_pie_sqt('D:\\成果转化\数据挖掘\DM_广中医\\13610215701外用\dst\定稿\\5_统计_四气_.xlsx', 'test.png')

from a_med_stand import read_excel_to_dict_list, save_dict_list_to_excel, medicine_stand
import os
from b_translate_feature import translate_feature, translate_feature_v2
from c_create_rect import creat_rect, extract_high_freq_columns
from d_statics import count_ones_in_columns, get_high_times, get_top_items
from d_connect_times import calculate_and_save_connect_similarities
from _baselib import modify_file_name, move_xlsx_to_result_folder,split_path_os

def dm1(src_file = 'data/test.xlsx'):
    # config
    dst_folder, filename = split_path_os(src_file)

    try:

        print('folder:', dst_folder, 'filename:', filename)
        min_med = 2
        max_med = 20
        do_med_stand = False
        high_row = 20

        # step1 药物标准化
        step1_file = 'step1.药物标准化后.xlsx'
        if do_med_stand:
            medicine_stand(src_file, step1_file, min_num=min_med, max_num=max_med)
        if not os.path.exists(step1_file):
            medicine_stand(src_file, step1_file, min_num=min_med, max_num=max_med)

        print('------------step1 finished------------')

        # stepX 证型标准化、症状标准化等
        # dst_file = 'StepX.证型标准化后.xlsx'

        # step2 四气、五味、归经、治法属性转换
        step2_file = 'step2.四气、五味、归经、治法属性转换.xlsx'
        translate_feature_v2(step1_file, step2_file)
        print('------------step2 finished------------')

        # step3 药物矩阵生成
        col_names = ['处方S']
        step3_1_file = 'step3.1药物矩阵_10.xlsx'
        step3_2_file = 'step3.2药物矩阵_YN.xlsx'
        step3_3_file = 'step3.3药物矩阵_类型.xlsx'
        creat_rect(step1_file, col_names, step3_1_file, step3_2_file, step3_3_file)
        print('------------step3 finished-')

        # step4 转换矩阵生成
        col_names = ['四气', '五味', '归经', '治法']
        step4_1_file = 'step4.1统计_10.xlsx'
        step4_2_file = 'step4.2统计_YN.xlsx'
        step4_3_file = 'step4.3统计.xlsx'
        creat_rect(step2_file, col_names, step4_1_file, step4_2_file, step4_3_file)
        modify_file_name(directory='./', prefix='step2.四气、五味、归经、治法属性转换_', replace_prefix='step4.统计矩阵_')
        print('------------step4 finished-')

        # step5 药物、性味归经、治法统计
        count_ones_in_columns('step4.统计矩阵_四气_10矩阵.xlsx', 'step5.四气统计.xlsx')
        count_ones_in_columns('step4.统计矩阵_五味_10矩阵.xlsx', 'step5.五味统计.xlsx')
        count_ones_in_columns('step4.统计矩阵_归经_10矩阵.xlsx', 'step5.归经统计.xlsx')
        count_ones_in_columns('step4.统计矩阵_治法_10矩阵.xlsx', 'step5.治法统计.xlsx')
        count_ones_in_columns('step3.1药物矩阵_10.xlsx', 'step5.药物统计.xlsx')

        calculate_and_save_connect_similarities('step3.1药物矩阵_10.xlsx', 'step6.药物连接度.xlsx')

        get_top_items('step5.药物统计.xlsx', 'step7.高频药物统计.xlsx', high_row - 1)
        get_top_items('step5.治法统计.xlsx', 'step7.高频治法统计.xlsx', high_row - 1)

        extract_high_freq_columns('step3.1药物矩阵_10.xlsx', 'step7.高频药物统计.xlsx', 'step8.高频药物矩阵10.xlsx')
        extract_high_freq_columns('step3.2药物矩阵_YN.xlsx', 'step7.高频药物统计.xlsx', 'step8.高频药物矩阵YN.xlsx')
        extract_high_freq_columns('step4.统计矩阵_治法_10矩阵.xlsx', 'step7.高频治法统计.xlsx',
                                  'step8.高频治法矩阵10.xlsx')
        extract_high_freq_columns('step4.统计矩阵_治法_YN矩阵.xlsx', 'step7.高频治法统计.xlsx',
                                  'step8.高频治法矩阵YN.xlsx')

        from d_cal_rules import calculate_rulues

        calculate_rulues('step1.药物标准化后.xlsx', 'step15.频繁项药物.xlsx', rules_file_path='step15.关联规则.xlsx',
                         min_support=0.1, min_confidence=0.8)
        from hcinpinyin import draw_rule

        draw_rule('step15.关联规则_for_draw.xlsx', 'step15.关联规则图和弦图.png')
        # 绘制四气饼图
        from hsqtpinyin import generat_pie_sqt

        generat_pie_sqt('step5.四气统计.xlsx', 'step13.四气饼图.png')

        from e_pcapinyin import pca_analysis

        pca_analysis('step8.高频药物矩阵10.xlsx', 'step9.药物PCA10.xlsx', 'step9.药物PCA.png',
                     'step9.药物PCA_upset.png',
                     'step9.药物PCA_per.png')

        temp1 = read_excel_to_dict_list('step7.高频药物统计.xlsx')
        high_times = 0
        for t1 in temp1:
            high_times = t1['times']
        from e_complex_networkpinyin import plot_complex_network

        plot_complex_network('step6.药物连接度.xlsx', 'step7.高频药物统计.xlsx', 'step10.药物复杂网络.png', high_times)

        from e_flusterpinyin import class_z_final

        class_z_final('step8.高频药物矩阵10.xlsx', 'step11.聚类结果.xlsx', 'step11.聚类')

        # 绘制高频药物词云图
        from hcytpinyin import generate_wordcloud_from_xlsx

        generate_wordcloud_from_xlsx('step7.高频药物统计.xlsx', 'step12.药物词云.png')
        generate_wordcloud_from_xlsx('step7.高频治法统计.xlsx', 'step12.治法词云.png')

        # 绘制归经雷达图1111111111111

        from hradarpinyin import generate_single_radar_chart

        generate_single_radar_chart('step5.五味统计.xlsx', 'step14.五味雷达图.png')
        generate_single_radar_chart('step5.归经统计.xlsx', 'step14.归经雷达图.png')

        from e_fisherpinyin import fisher
        src_file = r'step8.高频药物矩阵10.xlsx'
        dst_file = r'step16.显著性药对检验.xlsx'  # 指定输出文件路径
        fisher(src_file, 'step16.显著性药对检验.png', dst_file=dst_file)
        move_xlsx_to_result_folder(dst_folder=dst_folder)

        from _baselib import zip_dir,count_files_in_directory
        count_file =count_files_in_directory("D:\PhpProjects\SinoDigMed\dms")
        zip_dir(dst_folder,f'D:\PhpProjects\SinoDigMed\dms\\{count_file}.zip')
        return count_file

    except Exception as e:
        print(e)
        return None

if __name__ == '__main__':
    dm1()
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from upsetplot import plot  # 注意：这里我们直接从upsetplot导入plot函数，而不是UpSet类

# 设置Matplotlib支持中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 选择一个支持中文的字体，如SimHei
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

def convert_to_multiindex(db):
    # 定义一个函数来检查每个项目是否存在于给定的列表中
    items_to_check = []
    item_count = []
    for r in db:
        for c in r:
            if c not in items_to_check:
                items_to_check.append(c)
                item_count.append(1)
            else:
                idx = items_to_check.index(c)
                item_count[idx] = item_count[idx] +1

    def check_presence(item_list, items_to_check):
        return [item in item_list for item in items_to_check]

    multi_index_values = [check_presence(item_list, items_to_check) for item_list in db]
    print(multi_index_values,item_count)
    dst = []
    dst_num = []
    for m in multi_index_values:
        if m not in dst:
            dst.append(m)
            dst_num.append(1)
        else:
            idx = dst.index(m)
            dst_num[idx] = dst_num[idx] + 1
    print(dst, dst_num)

    # 创建 MultiIndex
    index = pd.MultiIndex.from_tuples(dst, names=items_to_check)

    return index, dst_num

def draw_up_set(db,upset_png_name='upset_plot.png'):
    # 测试数据
    # 调用函数并打印结果
    index, data = convert_to_multiindex(db)
    # 将数据和索引组合成一个DataFrame
    df = pd.DataFrame({'value': data}, index=index)
    series = df['value']
    print(series)
    # 绘制UpSet图，设置显示交集大小，并指定图表背景颜色
    plot(series, show_counts=True, facecolor="green")
    # 添加图表标题


    # 保存图表为PDF文件
    plt.savefig(upset_png_name)
    # 显示图表（注意：在某些环境中，如Jupyter Notebook，这一步可能是可选的）


import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori


def find_frequent_itemsets(db):
    # 转换数据格式
    te = TransactionEncoder()
    te_ary = te.fit(db).transform(db)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # 计算最小支持度
    total_transactions = len(db)
    min_support_value = 2 / total_transactions

    # 应用Apriori算法
    frequent_itemsets = apriori(df, min_support=min_support_value, use_colnames=True)

    # 初始化空列表用于存储频繁项集
    fre = []

    # 按行处理频繁项集
    for index, row in frequent_itemsets.iterrows():
        itemset = list(row['itemsets'])
        count = round(row['support'] * total_transactions)

        # 只添加包含多于一个项目的频繁项集
        if len(itemset) > 1:
            fre.append({'itemset':itemset,'count':count})

    return fre


# 调用函数
if __name__ == '__main__':
    db = [['酸枣仁', '甘草', '大枣'],
          ['酸枣仁', '党参', '甘草'],
          ['酸枣仁', '党参', '大枣'],
          ['酸枣仁', '黄精', '甘草'],
          ['党参', '甘草', '大枣']]
    draw_up_set(db)
    result = find_frequent_itemsets(db)
    print(result)

import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pymysql
from _baselib import split_path_os


def update_record_status_and_url(saved_filename, new_status, new_url):
    # 数据库连接信息
    db_config = {
        'host': '127.0.0.1',  # 如果数据库在本地服务器上
        'port': 3306,  # MySQL默认端口
        'user': 'root',
        'password': 'root1234',
        'database': 'web8',
        'charset': 'utf8mb4'  # 支持更多的字符集，比如emoji
    }

    # SQL 更新语句
    update_sql = """
    UPDATE dataminer_upload_records
    SET status = %s, url = %s
    WHERE saved_filename = %s
    """

    try:
        # 建立数据库连接
        connection = pymysql.connect(**db_config)

        with connection.cursor() as cursor:
            # 执行SQL语句
            affected_rows = cursor.execute(update_sql, (new_status, new_url, saved_filename))

            # 提交更改
            connection.commit()

        # 关闭连接
        connection.close()

        if affected_rows > 0:
            print(f"成功更新 {affected_rows} 行记录")
        else:
            print("没有找到匹配的记录进行更新")

    except pymysql.MySQLError as e:
        print(f"数据库错误：{e}")
        # 在发生错误时可以尝试回滚
        if 'connection' in locals():
            connection.rollback()
        raise


# 使用示例
# update_record_status_and_url('example_saved_filename.txt', 'processed', 'http://example.com/path/to/file')
from main import dm1


class ChangeHandler(FileSystemEventHandler):
    """定义处理文件变化的类"""

    def on_created(self, event):
        if not event.is_directory:
            print(f"Created file: {event.src_path}")

    def on_modified(self, event):
        if not event.is_directory:
            print(f"Modified file: {event.src_path}")
            folder, filename = split_path_os(event.src_path)
            time.sleep(5)  # 延迟一秒，等待文件写入完成
            print(f"文件 {filename} 已写入，开始更新数据库记录")
            import os
            if not os.path.exists(f'D:\PhpProjects\SinoDigMed\dmdata\\{filename[:-5]}'):
                os.makedirs(f'D:\PhpProjects\SinoDigMed\dmdata\\{filename[:-5]}')
                # 移动文件到指定文件夹
                os.rename(event.src_path, f'D:\PhpProjects\SinoDigMed\dmdata\\{filename[:-5]}\\{filename}')
                update_record_status_and_url(filename, '已接收', '...')
                result = dm1(f'D:\PhpProjects\SinoDigMed\dmdata\\{filename[:-5]}\\{filename}')
                if result is not None:
                    print(f"文件 {filename} 已处理完成，开始更新数据库记录")
                    update_record_status_and_url(filename, '处理成功', f'http://localhost/dms/{result}.zip')
                else:
                    print(f"文件 {filename} 处理失败，请检查日志")
                    update_record_status_and_url(filename, '处理失败，请按模板上传', '...')

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"Deleted file: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"Moved file from {event.src_path} to {event.dest_path}")


def start_monitoring(path_to_watch='D:\\dataminer'):
    """启动对指定路径的监控"""
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path_to_watch, recursive=True)
    print(f"Starting monitoring on {path_to_watch}")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping monitoring.")
    finally:
        observer.stop()
        observer.join()


if __name__ == "__main__":
    # 调用函数开始监控
    start_monitoring()

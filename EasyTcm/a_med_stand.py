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

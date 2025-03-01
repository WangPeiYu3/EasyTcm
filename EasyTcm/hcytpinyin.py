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


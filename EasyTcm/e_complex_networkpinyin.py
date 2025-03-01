import matplotlib
matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
import matplotlib.pyplot as plt

import numpy as np
import math
import itertools
import random
import pandas as pd
from pypinyin import pinyin, lazy_pinyin  # 导入拼音库

# 设置字体以便正确显示中文标签
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


def gradient_color(value, start_color, end_color):
    """从浅色渐变到深色"""
    if value < 0 or value > 1:
        raise ValueError("Value must be between 0 and 1")
    if value < 0.3:
        value = 0.3

    r = int(start_color[0] + (end_color[0] - start_color[0]) * value)
    g = int(start_color[1] + (end_color[1] - start_color[1]) * value)
    b = int(start_color[2] + (end_color[2] - start_color[2]) * value)

    return "#{:02X}{:02X}{:02X}".format(r, g, b)


def shuffle_associated_arrays(arr1, arr2):
    """将两个数组关联起来并随机排序"""
    if len(arr1) != len(arr2):
        raise ValueError("两个数组的长度必须相同")

    combined_list = list(zip(arr1, arr2))
    random.shuffle(combined_list)

    shuffled_arr1, shuffled_arr2 = zip(*combined_list)

    return list(shuffled_arr1), list(shuffled_arr2)


def convert_to_pinyin(text):
    """将中文转换为拼音"""
    return ''.join([p.capitalize() for p in lazy_pinyin(text)])


def plot_complex_network(file1, file2, save_path, high_times=19, col_name='处方S'):
    # 读取Excel文件
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    dict_array1 = df1.to_dict(orient='records')
    dict_array2 = df2.to_dict(orient='records')

    label_text = []
    label_count = []
    for d in dict_array2:
        if d['times'] >= high_times:
            label_text.append(d['Item3'])
            label_count.append(d['times'])

    max_times = max(label_count)

    # 设置图形大小为20cm x 20cm，分辨率为300dpi
    fig, ax = plt.subplots(figsize=(28 / 2.54, 28 / 2.54), dpi=300)
    ax.axis('off')

    width_in_pixels = fig.get_size_inches()[0] * fig.dpi
    height_in_pixels = fig.get_size_inches()[1] * fig.dpi

    center_x, center_y = width_in_pixels / 2, height_in_pixels / 2
    radius_in_pixels = 12 * 300 / 2.54
    circle_radius_in_pixels = 1.8 * 300 / 2.54

    N = len(label_text)
    print(N)
    angles = np.linspace(0, 2 * math.pi, N + 1)[:-1]
    label_text, label_count = shuffle_associated_arrays(label_text, label_count)

    centers = []

    for angle, count in zip(angles, label_count):
        x = center_x + radius_in_pixels * math.cos(angle)
        y = center_y + radius_in_pixels * math.sin(angle)

        centers.append((x, y))

        rad = circle_radius_in_pixels * count / max_times
        alp = count / max_times
        color = gradient_color(alp, (255, 255, 204), (225, 25, 25))
        color = 'red'

        circle = plt.Circle((x, y), rad, color=color, fill=True,
                            linewidth=0, alpha=alp)
        ax.add_artist(circle)

        label_x = x
        label_y = y
        fs = 20 * count / max_times
        fs = max(fs, 12)

        # 将中文转换为拼音
        pinyin_label = convert_to_pinyin(label_text[centers.index((x, y))])

        ax.text(label_x, label_y, pinyin_label, ha='center', va='center', fontsize=fs,
                color='black')

    connect = [d for d in dict_array1 if d['Item1'] in label_text and d['Item2'] in label_text]
    max_con = max(d['connect'] for d in connect)

    for center1, center2 in itertools.combinations(centers, 2):
        center1_idx = centers.index(center1)
        center2_idx = centers.index(center2)

        cur_connect = next((c['connect'] for c in connect if
                            (c['Item1'] == label_text[center1_idx] and c['Item2'] == label_text[center2_idx]) or
                            (c['Item2'] == label_text[center1_idx] and c['Item1'] == label_text[center2_idx])), 0)

        lw = cur_connect / max_con * 8
        alp = cur_connect / max_con
        color = gradient_color(alp, (48, 190, 60), (48, 190, 195))
        color = '#46b7b9'
        ax.plot([center1[0], center2[0]], [center1[1], center2[1]], color, linewidth=lw, alpha=alp)

    ax.set_xlim([0, width_in_pixels])
    ax.set_ylim([0, height_in_pixels])

    plt.savefig(save_path, dpi=300, bbox_inches='tight', pad_inches=0)
    plt.close()


# 调用函数
if __name__ == '__main__':
    file1 = 'D:\\成果转化\\数据挖掘\\DM_广中医\\13610215701外用\\dst\\定稿\\6_共现网络.xlsx'
    file2 = 'D:\\成果转化\\数据挖掘\\DM_广中医\\13610215701外用\\dst\\定稿\\6_类型频次.xlsx'
    save_path = "circles_with_all_lines_between_centers_pinyin.png"
    plot_complex_network(file1, file2, save_path, high_times=17)

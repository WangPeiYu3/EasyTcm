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
    font = FontProperties(fname=r"C:\Windows\Fonts\arial.ttf", size=6)

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
    # plt.savefig(save_path, dpi=600)
    plt.savefig(save_path.replace('.png', '.svg'), format='svg')

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

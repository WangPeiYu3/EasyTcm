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
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
import random

def read_csv_to_dict_list(file_path):
    try:
        if file_path.endswith('.csv'):
            # 读取CSV文件
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            # 读取Excel文件
            df = pd.read_excel(file_path)
        else:
            print("Unsupported file format. Only CSV and XLSX are supported.")
            return None

        # 将DataFrame转换为字典列表
        data_dict_list = df.to_dict(orient='records')

        return data_dict_list
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
def generate_warm_color():
    # 随机生成 RGB 值，确保色调在暖色系范围内
    red = random.randint(200, 255)  # 控制红色通道在较高范围
    green = random.randint(50, 150)  # 控制绿色通道在中等范围
    blue = random.randint(0, 100)  # 控制蓝色通道在较低范围

    return red, green, blue


def generate_cool_color():
    # 随机生成 RGB 值，确保色调在冷色系范围内
    red = random.randint(0, 100)  # 控制红色通道在较低范围
    green = random.randint(100, 200)  # 控制绿色通道在中等范围
    blue = random.randint(180, 255)  # 控制蓝色通道在较高范围

    return red, green, blue


def generate_neutral_color():
    # 随机生成 RGB 值，确保色调在平色系范围内
    red = random.randint(100, 200)  # 控制红色通道在中等范围
    green = random.randint(100, 200)  # 控制绿色通道在中等范围
    blue = random.randint(100, 200)  # 控制蓝色通道在中等范围

    return red, green, blue



def generate_transparent_colors1(color):
    # Splitting the RGB color components and normalizing them
    r, g, b = [component / 255 for component in color]

    # Generating colors with different opacities
    transparent_colors = []
    for index in range(5):
        tra = index / 5 + 0.1
        transparent_colors.append((r, g, b, tra))

    return transparent_colors


def generate_transparent_colors2(color):
    # Splitting the RGB color components and normalizing them
    r, g, b = [component / 255 for component in color]

    # Generating colors with different opacities
    transparent_colors = []
    for index in range(5):
        tra = 1 - index / 5 - 0.1
        transparent_colors.append((r, g, b, tra))

    return transparent_colors




def generat_pie_pic(ping_color, hot_color, cold_color,save_path,labels,sizes):
    plt.clf()
    plt.cla()
    plt.close()
    color_s = []
    ping_color_rgba = (ping_color[0] / 255, ping_color[1] / 255, ping_color[2] / 255, 0.5)
    color_s.append(ping_color_rgba)
    color_s += generate_transparent_colors2(hot_color)
    color_s += generate_transparent_colors1(cold_color)
    # 找到类别2的索引
    category2_index = labels.index('平')
    start_angle = -float(sizes[0]) / sum(sizes) * 180
    # 生成explode列表
    explode = [0 if i == category2_index else 0 for i in range(len(labels))]
    # 设置中文字体为微软雅黑
    font = FontProperties(fname=r"c:\windows\fonts\msyh.ttc", size=6)

    # 绘制饼状图，将类别2放在最右侧并使其扇形中心线水平
    patches, texts, autotexts = plt.pie(sizes, explode=explode, colors=color_s, autopct='%1.2f%%', shadow=False,
            startangle=start_angle,
            textprops={'fontproperties': font}, rotatelabels=False)

    plt.axhline(y=0, color='black', linestyle='--', linewidth=2)

    # 添加图例
    plt.legend(patches, ['%s, %1.2f %%' % (l, s / sum(sizes) * 100) for l, s in zip(labels, sizes)],
               loc='lower right', fontsize=8, prop=font)

    # 隐藏自动文本（即百分比）
    for autotext in autotexts:
        autotext.set_visible(False)
    # 设置图标题
    # plt.title('四气图', fontproperties=font)
    # 设置坐标轴相等，以保持图形的正圆形状

    plt.axis('equal')
    plt.savefig(save_path, dpi=600)
    plt.close()





def generat_pie_sqt(sq_file,save_path):
    # 数据
    labels = ['平', '大热', '热', '微热', '温', '微温', '微凉', '凉', '微寒', '寒', '大寒']
    sizes = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    dict_list = read_csv_to_dict_list(sq_file)

    for si in labels:
        index = labels.index(si)
        for sq in dict_list:
            if sq['Item3'] == labels[index]:
                sizes[index] = sq['times']

    light_blue_rgb1 = (0, 191, 255)
    hot_color = (255, 0, 0)
    cold_color = (0, 255, 0)
    generat_pie_pic(light_blue_rgb1, hot_color, cold_color, f'{save_path}',labels,sizes)



if __name__ == '__main__':
    generat_pie_sqt('D:\\成果转化\数据挖掘\DM_广中医\\13610215701外用\dst\定稿\\5_统计_四气_.xlsx',
                    'test.png')
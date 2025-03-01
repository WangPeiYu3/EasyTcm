import sys
import random
from pycirclize import Circos
import pandas as pd

# 设置Matplotlib支持中文


def generate_matrix(rows, cols):
    # 创建一个空的列表来存储矩阵
    matrix_data = []

    # 使用嵌套循环来生成矩阵
    for _ in range(rows):
        row = [0] * cols
        matrix_data.append(row)

    return matrix_data

def get_data(file_path,min_sups=0,min_con = 0,mod = '支持度'):
    df = pd.read_excel(file_path)
    data_dict_list = df.to_dict(orient='records')
    row_names = []
    for r in data_dict_list:
        sup = float(r['支持度百分比'])
        con = float(r['置信度百分比'])
        if sup >= min_sups >0 and con>=min_con>0:
            if (r[list(r.keys())[0]]) not in row_names:
                row_names.append((r[list(r.keys())[0]]))
            if r[list(r.keys())[1]] not in row_names:
                row_names.append(r[list(r.keys())[1]])


    matrix_data = generate_matrix(len(row_names), len(row_names))
    for r in data_dict_list:
        row_ = r[list(r.keys())[0]]
        col_ = r[list(r.keys())[1]]
        sup = float(r['支持度百分比'])
        con = float(r['置信度百分比'])
        if sup >= min_sups >0 and con>=min_con>0:
            idx_row = row_names.index(row_)
            idx_col = row_names.index(col_)
            if mod == '支持度':
                matrix_data[idx_row][idx_col] = sup
            if mod == '置信度':
                matrix_data[idx_row][idx_col] = con
    return matrix_data,row_names

def draw_rule(file_path,png_path,min_sup=1,min_con=1,mod='置信度'):
    import matplotlib
    matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
    import matplotlib.pyplot as plt

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
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
    file_path = "rules_for_draw.xlsx"
    png_path = 'chord_diagram.png'
    min_sup = 1
    min_con = 1
    mod = '置信度'
    draw_rule(file_path,png_path,min_sup,min_con,mod)


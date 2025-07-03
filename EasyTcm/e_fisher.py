import pandas as pd
from scipy.stats import fisher_exact
import numpy as np
import seaborn as sns



def fisher(file_path, png_file, dst_file='', cmap='viridis'):
    import matplotlib

    matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
    import matplotlib.pyplot as plt
    # 使用pandas读取Excel文件
    df = pd.read_excel(file_path)
    # 获取列名列表
    columns = df.columns.tolist()
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
    co_occurrence_df = pd.DataFrame(index=columns, columns=columns, dtype=float).fillna(0)
    # 创建一个DataFrame来存储p值
    p_values_df = pd.DataFrame(index=columns, columns=columns, dtype=float).fillna(1)  # 默认填充为1，表示不显著

    # 填充共现率和p值的DataFrame
    for (col1, col2), result in results.items():
        co_occurrence_df.at[col1, col2] = result['co-occurrence_rate']
        p_values_df.at[col1, col2] = result['p-value']

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

    # 创建一个掩码，用于隐藏下半部分以及值为0的部分
    mask = np.tril(np.ones_like(co_occurrence_df, dtype=bool))

    # 绘制热图
    plt.figure(figsize=(16, 12))
    ax = sns.heatmap(co_occurrence_df, annot=True, cmap=cmap, mask=mask, fmt='.2f')

    # 遍历p_values_df，找到所有p-value < 0.05的单元格并在热图上标记
    significant_pairs = []
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            if p_values_df.iloc[i, j] < 0.05:
                # 在热图对应位置添加红色实心圆
                ax.plot(j + 0.5, i + 0.8, 'ro', markersize=7, markeredgewidth=0)
                # 收集显著性组合
                significant_pairs.append({
                    'Column 1': columns[i],
                    'Column 2': columns[j],
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

    plt.savefig(png_file,dpi=300,bbox_inches='tight')

    # 将显著性组合写入文件
    if dst_file:
        # 将显著性组合转换为DataFrame
        significant_df = pd.DataFrame(significant_pairs)
        # 写入CSV文件
        significant_df.to_excel(dst_file, index=False)
        print(f"Significant pairs have been written to {dst_file}")


# 示例调用
if __name__ == '__main__':
    src_file = r'D:\成果转化\数据挖掘\樱桃小丸子明\dst\定稿\9_高频关联矩阵_处方S_10矩阵.xlsx'
    dst_file = r'显著性药对.xlsx'  # 指定输出文件路径
    fisher(src_file, '显著性药对检验.svg', dst_file=dst_file)
import pandas as pd
from scipy.stats import fisher_exact
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pypinyin import pinyin, Style
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Arial']  # 设置字体为 Arial
matplotlib.rcParams['axes.unicode_minus'] = False  # 避免负号显示为方块
# 将中文转换为拼音
def chinese_to_pinyin(chinese_text):
    pinyin_text = pinyin(chinese_text, style=Style.NORMAL)
    return ''.join([word[0].capitalize() for word in pinyin_text])  # 提取拼音的首字母并连接成字符串

def fisher(file_path, png_file, dst_file='', cmap='viridis'):
    # 读取Excel文件
    df = pd.read_excel(file_path)
    columns = df.columns.tolist()
    columns_pinyin = [chinese_to_pinyin(col) for col in columns]  # 列名转换为拼音

    results = {}
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            table = pd.crosstab(df[columns[i]], df[columns[j]])
            try:
                oddsratio, p_value = fisher_exact(table)
                co_occurrence_rate = table.loc[1, 1] / table.sum().sum()
                results[(columns[i], columns[j])] = {
                    'oddsratio': oddsratio,
                    'p-value': p_value,
                    'co-occurrence_rate': co_occurrence_rate
                }
            except ValueError as e:
                results[(columns[i], columns[j])] = {'error': str(e)}

    co_occurrence_df = pd.DataFrame(index=columns_pinyin, columns=columns_pinyin, dtype=float).fillna(0)
    p_values_df = pd.DataFrame(index=columns_pinyin, columns=columns_pinyin, dtype=float).fillna(1)

    for (col1, col2), result in results.items():
        co_occurrence_df.at[chinese_to_pinyin(col1), chinese_to_pinyin(col2)] = result['co-occurrence_rate']
        p_values_df.at[chinese_to_pinyin(col1), chinese_to_pinyin(col2)] = result['p-value']

    plt.figure(figsize=(18, 14))  # 增大图像尺寸
    ax = sns.heatmap(
        co_occurrence_df, annot=True, cmap=cmap, mask=np.tril(np.ones_like(co_occurrence_df, dtype=bool)),
        fmt='.2f', annot_kws={"size": 10}  # 调整字体大小
    )

    # 标记显著性 p < 0.05 的值
    for i in range(len(columns_pinyin)):
        for j in range(i + 1, len(columns_pinyin)):
            if p_values_df.iloc[i, j] < 0.05:
                ax.text(j + 0.5, i + 0.5, '*', color='red', fontsize=12, ha='center', va='center', fontweight='bold')

    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=12)  # 旋转 x 轴标签
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=12)  # 保持 y 轴标签水平
    ax.xaxis.set_ticks_position('top')  # 将 x 轴标签放置在顶部
    ax.xaxis.set_label_position('top')

    plt.savefig(png_file, dpi=300, bbox_inches='tight')

    if dst_file:
        significant_pairs = [
            {
                'Column 1': columns_pinyin[i],
                'Column 2': columns_pinyin[j],
                'Odds Ratio': round(results[(columns[i], columns[j])]['oddsratio'], 4),
                'P-value': round(results[(columns[i], columns[j])]['p-value'], 4),
                'Co-occurrence Rate': round(results[(columns[i], columns[j])]['co-occurrence_rate'], 4)
            }
            for i in range(len(columns_pinyin))
            for j in range(i + 1, len(columns_pinyin))
            if p_values_df.iloc[i, j] < 0.05
        ]
        pd.DataFrame(significant_pairs).to_excel(dst_file, index=False)

# 示例调用
if __name__ == '__main__':
    fisher('data.xlsx', '优化后的显著性药对检验.svg', dst_file='显著性药对.xlsx')
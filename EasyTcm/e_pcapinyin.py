import json
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import itertools
import plotly.graph_objects as go
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['svg.fonttype'] = 'none'  # 保证 SVG 中字体可编辑
plt.rcParams['axes.unicode_minus'] = False

from pypinyin import lazy_pinyin
from upset import draw_up_set, find_frequent_itemsets
from a_med_stand import save_dict_list_to_excel

def chinese_to_pinyin(text):
    return ''.join([p.capitalize() for p in lazy_pinyin(text)])

def pca_analysis(
    file_path,
    output_xlsx='pca.xlsx',
    pca3d_path='pca3d.svg',
    upset_path='upset.svg',
    variance_path='variance.svg',
    percentile=0.8
):
    # Step 1: 读取数据并标准化
    df = pd.read_excel(file_path)
    feature_names = [chinese_to_pinyin(name) for name in df.columns]
    X = df.values
    X_scaled = StandardScaler().fit_transform(X)

    # Step 2: PCA分析
    pca = PCA(n_components=min(len(feature_names), len(X)))
    X_pca = pca.fit_transform(X_scaled)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    min_components = np.argmax(cumulative_variance >= percentile) + 1

    # Step 3: 提取主成分关键特征
    ven_arr = []
    component_arr = []
    for i, component in enumerate(pca.components_[:min_components]):
        component_series = pd.Series(component, index=feature_names).abs().sort_values(ascending=False)
        top_8 = component_series.head(8)
        ven_arr.append(list(top_8.index))
        component_arr.append(component_series.to_dict())
        print(f"Component {i + 1}:", component_series.to_dict())

    save_dict_list_to_excel(component_arr, output_xlsx)
    print(pd.DataFrame({'features': ven_arr}))

    # Step 4: 方差解释率图（保存为 SVG）
    plt.figure(figsize=(8, 6))
    plt.bar(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_ * 100, alpha=0.5)
    plt.step(range(1, len(cumulative_variance) + 1), cumulative_variance * 100, where='mid', label='Cumulative Variance')
    plt.axhline(y=80, color='r', linestyle='--', label='80% Explained Variance')
    plt.axvline(x=min_components, color='g', linestyle='--', label=f'Min Components: {min_components}')
    plt.ylabel('Explained Variance (%)')
    plt.xlabel('Principal Component')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(variance_path, format='svg')
    plt.close()


    x_loadings = pca.components_[0]
    y_loadings = pca.components_[1]
    z_loadings = pca.components_[2]

    def generate_label_offsets(x, y, z, min_dist=0.08):
        n = len(x)
        offsets = [(0, 0, 0)] * n
        for i in range(n):
            for j in range(i):
                dist = np.linalg.norm([
                    x[i] + offsets[i][0] - x[j] - offsets[j][0],
                    y[i] + offsets[i][1] - y[j] - offsets[j][1],
                    z[i] + offsets[i][2] - z[j] - offsets[j][2]
                ])
                if dist < min_dist:
                    dx, dy, dz = np.random.uniform(-0.02, 0.02, size=3)
                    offsets[i] = (offsets[i][0] + dx,
                                offsets[i][1] + dy,
                                offsets[i][2] + dz)
        return offsets

    # -------- 重叠检测函数 --------
    def find_close_labels(x, y, z, names, threshold=0.07):
        close_pairs = []
        for i, j in itertools.combinations(range(len(x)), 2):
            dist = np.linalg.norm([x[i] - x[j], y[i] - y[j], z[i] - z[j]])
            if dist < threshold:
                close_pairs.append((names[i], names[j]))
        return close_pairs

    # -------- 手动微调（可空，可后续添加）--------
    manual_offsets = {
        "FuShen": (0.025, 0.015, 0.015),
        "MuLi": (-0.02, -0.01, -0.01),
        "ChuanXiong": (-0.03, 0.02, 0.01),     # 再往右下偏一些
        "BaiShao": (-0.025, -0.02, -0.05),      # 再往左上偏一些
        "DangShen": (0.025, 0.02, 0.015),      # 上移 + 右偏
        "HuangQi": (-0.025, -0.02, -0.015)     # 下移 + 左偏
    }


    # 创建图形
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # 绘制散点
    sc = ax.scatter(x_loadings, y_loadings, z_loadings,
                    c=z_loadings, cmap='viridis', s=60,
                    edgecolors='black', alpha=0.9)

    # 自动偏移
    label_offsets = generate_label_offsets(x_loadings, y_loadings, z_loadings)

    # 添加标签（自动 + 手动叠加）
    for i, name in enumerate(feature_names):
        dx, dy, dz = label_offsets[i]
        mdx, mdy, mdz = manual_offsets.get(name, (0, 0, 0))
        ax.text(x_loadings[i] + dx + mdx,
                y_loadings[i] + dy + mdy,
                z_loadings[i] + dz + mdz,
                name,
                fontsize=10,
                color='darkred',
                ha='center', va='bottom')

    # 坐标轴和外观设置
    ax.set_xlabel("PC1", fontsize=14, labelpad=10)
    ax.set_ylabel("PC2", fontsize=14, labelpad=10)
    ax.set_zlabel("PC3", fontsize=14, labelpad=10)
    ax.xaxis.pane.set_facecolor((1, 1, 1, 1))
    ax.yaxis.pane.set_facecolor((1, 1, 1, 1))
    ax.zaxis.pane.set_facecolor((1, 1, 1, 1))
    ax.xaxis._axinfo["grid"]["color"] = (0.8, 0.8, 0.8, 0.6)
    ax.yaxis._axinfo["grid"]["color"] = (0.8, 0.8, 0.8, 0.6)
    ax.zaxis._axinfo["grid"]["color"] = (0.8, 0.8, 0.8, 0.6)
    ax.view_init(elev=25, azim=135)

    # -------- 输出建议手动调整的标签对 --------
    close_pairs = find_close_labels(x_loadings, y_loadings, z_loadings, feature_names)
    if close_pairs:
        print("⚠️ 以下标签彼此距离过近，建议在 manual_offsets 中微调：")
        for a, b in close_pairs:
            print(f"  - '{a}' 和 '{b}'")
    else:
        print("✅ 无明显标签重叠，无需手动微调。")

    # 保存图像
    plt.tight_layout()
    plt.savefig("pca_3d.svg", format="svg")
    # Step 6: 频繁项集分析 & UpSet 图
    fre = find_frequent_itemsets(ven_arr)
    draw_up_set(ven_arr, upset_path)
    max_count = max(f['count'] for f in fre)
    for f in fre:
        if f['count'] == max_count:
            print("Most frequent set:", f)

if __name__ == '__main__':
    pca_analysis(
        file_path='step8.高频药物矩阵10.xlsx',
        output_xlsx='step9.药物PCA10.xlsx',
        pca3d_path='step9.药物PCA3D.svg',
        upset_path='step9.药物PCA_upset.svg',
        variance_path='step9.药物PCA_variance.svg'
    )

#后续修改方式：1设置累计贡献率阈值，根据累计贡献率计算降维数量，计算每个PCA中特征重要性最大的前5种药
import json
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
from upset import draw_up_set, find_frequent_itemsets
from a_med_stand import save_dict_list_to_excel

def pca_analysis(
    file_path,
    output_xlsx='pca.xlsx',
    pca3d_svg='pca3d.svg',
    upset_svg='upset.svg',
    rat_svg='rat.svg',
    percentile=0.8
):
    import pandas as pd
    df = pd.read_excel(file_path)

    feature_names = df.columns
    X = df.values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    n_components = min(len(feature_names), len(feature_names))
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)

    print("Eigenvalues (Explained Variance):", pca.explained_variance_)
    print("Variance Ratio (%):", pca.explained_variance_ratio_ * 100)
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    print("Cumulative Variance (%):", cumulative_variance * 100)

    min_components = np.argmax(cumulative_variance >= percentile) + 1

    print("\nFeature vectors (components):")
    ven_arr = []
    component_arr = []

    for i, component in enumerate(pca.components_):
        if i < min_components:
            component_series = pd.Series(component, index=feature_names).abs().sort_values(ascending=False)
            top_8_features = component_series.head(8)
            top_8_json = json.loads(top_8_features.to_json(force_ascii=False, indent=4))
            ven_arr.append(list(top_8_json.keys()))
            print(f"Component {i + 1}: {dict(component_series)}")
            component_arr.append(dict(component_series))

    save_dict_list_to_excel(component_arr, output_xlsx)

    df_result = pd.DataFrame({'features': ven_arr})
    print(df_result)

    # PCA 解释方差柱状图
    plt.figure(figsize=(8, 6))
    plt.bar(range(1, len(pca.explained_variance_ratio_) + 1),
            pca.explained_variance_ratio_ * 100, alpha=0.5, align='center')
    plt.step(range(1, len(cumulative_variance) + 1),
             cumulative_variance * 100, where='mid', label='Cumulative Variance')
    plt.axhline(y=80, color='r', linestyle='--', label='80% Explained Variance')
    plt.axvline(x=min_components, color='g', linestyle='--', label=f'Min Components for >=80% ({min_components})')
    plt.ylabel('Explained Variance (%)')
    plt.xlabel('Principal Component')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(rat_svg, format='svg')

    # 3D Loadings 图
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    x_loadings = pca.components_[0]
    y_loadings = pca.components_[1]
    z_loadings = pca.components_[2]

    for i in range(len(x_loadings)):
        ax.text(x_loadings[i], y_loadings[i], z_loadings[i], feature_names[i], color="red")

    ax.scatter(x_loadings, y_loadings, z_loadings)
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    plt.savefig(pca3d_svg, format='svg')

    print(ven_arr)
    fre = find_frequent_itemsets(ven_arr)
    draw_up_set(ven_arr, upset_svg)

    max_count = max(f['count'] for f in fre)
    for f in fre:
        if f['count'] == max_count:
            print(f)

    plt.close()

if __name__ == '__main__':
    pca_analysis('result/step8.高频药物矩阵10.xlsx')
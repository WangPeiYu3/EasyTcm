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

def pca_analysis(file_path,output_xlsx='pca.xlsx',pca3d_png='pca3d.png',upset_png='upset.png',rat_png='rat.png',percentile=0.8):
    import pandas as pd
    # 读取 Excel 文件
    df = pd.read_excel(file_path)
    # 获取特征名称（第一行作为列名）
    feature_names = df.columns
    # 获取数据部分（去掉第一行）
    X = df.values
    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # 创建 PCA 模型
    n_components = min(len(feature_names), len(feature_names))  # 至少需要3个主成分来绘制3D图
    pca = PCA(n_components=n_components)
    # 拟合模型并转换数据
    X_pca = pca.fit_transform(X_scaled)
    # 输出特征值（每个主成分的方差）
    print("Eigenvalues (Explained Variance):", pca.explained_variance_)
    # 输出方差百分比
    print("Variance Ratio (%):", pca.explained_variance_ratio_ * 100)
    # 计算累计方差百分比
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    print("Cumulative Variance (%):", cumulative_variance * 100)
    min_components = np.argmax(cumulative_variance >= percentile) + 1

    up_set_arr = []
    # 输出特征向量
    print("\nFeature vectors (components):")
    ven_arr = []
    component_arr = []
    for i, component in enumerate(pca.components_):
        if i < min_components:
            # 将特征向量转换为 Pandas Series，并按绝对值排序
            component_series = pd.Series(component, index=feature_names).abs().sort_values(ascending=False)


            # 输出绝对值最大的8项
            top_8_features = component_series.head(8)
            top_8_json = json.loads(top_8_features.to_json(force_ascii=False, indent=4))
            ven_arr.append(list(top_8_json.keys()))
            print(f"Component {i + 1}: {dict(component_series)}")
            component_arr.append(dict(component_series))
    save_dict_list_to_excel( component_arr,output_xlsx)
    # 将数据转换为 DataFrame
    df = pd.DataFrame({
        'features': ven_arr
    })
    print(df)

    # 查找累积解释方差大于等于80%所需的最小主成分数
    # 可视化 PCA 结果
    plt.figure(figsize=(8, 6))
    plt.bar(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_ * 100, alpha=0.5,
            align='center')
    plt.step(range(1, len(cumulative_variance) + 1), cumulative_variance * 100, where='mid',
             label='Cumulative Variance')
    plt.axhline(y=80, color='r', linestyle='--', label='80% Explained Variance')  # 添加水平线
    # 绘制垂直线
    plt.axvline(x=min_components, color='g', linestyle='--', label=f'Min Components for >=80% ({min_components})')

    plt.ylabel('Explained Variance (%)')
    plt.xlabel('Principal Component')
    plt.legend(loc='best')
    plt.tight_layout()
    plt.savefig(rat_png,dpi=300)

    # 绘制3D载荷图
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
    # plt.title('3D Loadings Plot')
    plt.savefig(pca3d_png,dpi=300)
    print(ven_arr)
    fre = find_frequent_itemsets(ven_arr)
    draw_up_set(ven_arr, upset_png)
    max = 1
    for f_ in fre:
        if f_['count'] > max:
            max = f_['count']
    for f_ in fre:
        if f_['count'] == max:
            print(f_)
    plt.close()
if __name__ == '__main__':
    pca_analysis('result/step8.高频药物矩阵10.xlsx')



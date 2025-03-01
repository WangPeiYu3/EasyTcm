import matplotlib
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt
from a_med_stand import save_dict_list_to_excel
from pypinyin import lazy_pinyin  # 导入拼音库

matplotlib.use('TkAgg')  # 在导入 pyplot 之前设置后端
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']


def convert_to_pinyin(text):
    """将中文转换为拼音"""
    return ''.join([p.capitalize() for p in lazy_pinyin(text)])


def class_z(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 转置数据框以便对变量进行聚类
    transposed_df = df.T

    # 计算层次聚类
    Z = linkage(transposed_df, 'ward')

    # 提取所有节点间的距离，并去重
    distances = list(np.unique(Z[:, 2]))
    availuable = []
    for d in distances[1:]:
        d1 = distances[distances.index(d) - 1]
        availuable.append(round((d + d1) / 2, 2))

    return Z, transposed_df, availuable


def class_z2(file_path, line_dis, number, dst_png_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 转置数据框以便对变量进行聚类
    transposed_df = df.T

    # 计算层次聚类
    Z = linkage(transposed_df, 'ward')  # 使用ward方法
    base_count = len(transposed_df)

    # 获取列名作为标签
    labels = transposed_df.index.tolist()

    # 将标签转换为拼音
    labels_pinyin = [convert_to_pinyin(label) for label in labels]

    # 绘制水平方向的树状图
    plt.figure(figsize=(10, 7))
    dendro = dendrogram(Z, labels=labels_pinyin, orientation='right', leaf_font_size=8)
    plt.xlabel('Distance')
    plt.ylabel('Variable')

    # 获取y轴的范围
    y_lim = plt.ylim()

    # 查找距离为line_dis的位置并绘制垂直线
    distances = Z[:, 2]
    closest_distance_index = np.argmin(np.abs(distances - line_dis))
    closest_distance = distances[closest_distance_index]

    # 查找比最接近距离更小的下一个距离
    lower_distance = None
    upper_distance = None
    if closest_distance > line_dis:
        lower_distance = distances[np.max(np.where(distances < closest_distance))]
        upper_distance = closest_distance
    elif closest_distance < line_dis:
        upper_distance = distances[np.min(np.where(distances > closest_distance))]
        lower_distance = closest_distance
    else:
        # 如果最接近的距离正好等于line_dis，那么就绘制这条线
        idx = np.where(Z[:, 2] == closest_distance)[0][0]
        x = Z[idx, 2]
        plt.vlines(x=x, ymin=y_lim[0], ymax=y_lim[1], colors='r', linestyles='--', label=f'Distance {line_dis}')
        plt.legend()
        plt.savefig(f'{dst_png_path}_{number}.png')
        plt.close()
        return Z, transposed_df, [lower_distance, upper_distance]

    if lower_distance is not None and upper_distance is not None:
        # 在最接近的距离之间绘制竖线
        plt.vlines(x=(lower_distance + upper_distance) / 2, ymin=y_lim[0], ymax=y_lim[1],
                   colors='r', linestyles='--', label=f'Distance =  {line_dis}')
        plt.legend()

    plt.savefig(f'{dst_png_path}_{number}.png')
    plt.close()

    # 提取所有节点间的距离，并去重
    distances_unique = list(np.unique(Z[:, 2]))
    availuable = []
    for d in distances_unique[1:]:
        d1 = distances_unique[distances_unique.index(d) - 1]
        availuable.append(round((d + d1) / 2, 2))

    return Z, transposed_df, [lower_distance, upper_distance]


def get_number_of_clusters(Z, dis):
    from scipy.cluster.hierarchy import fcluster
    #
    flusters = fcluster(Z, dis, criterion='distance')
    unique_clusters = np.unique(flusters)
    return len(unique_clusters), flusters


def get_class_by_distance(distance_threshold, Z, transposed_df):
    num_clusters, cluster_assignment = get_number_of_clusters(Z, distance_threshold)

    # 创建一个新的 DataFrame 来存储簇分配信息
    cluster_df = pd.DataFrame({'Cluster': cluster_assignment, 'Variable': transposed_df.index})

    # 使用 groupby 方法来根据簇号对变量进行分组
    grouped = cluster_df.groupby('Cluster')

    class_dst = []
    max_count = 0
    min_count = 100
    # 输出每个簇中的变量
    for cluster_id, group in grouped:
        class_dst.append({'Cluster': cluster_id, 'values': group['Variable'].to_list()})
        if len(group['Variable'].values) > max_count:
            max_count = len(group['Variable'].values)

        if len(group['Variable'].values) < min_count:
            min_count = len(group['Variable'].values)

    return num_clusters, class_dst, max_count - min_count


# 使用示例


def class_z_final(file_path, dst_xls_path='step11_dst.xlsx', dst_png_path='cluster', mim_num_clusters=4,
                 max_num_clusters=8):
    Z, df, values = class_z(file_path)
    result = []
    for d in values:
        num_clusters, dst_class, de_count = get_class_by_distance(d, Z, df)
        if mim_num_clusters <= num_clusters <= max_num_clusters:
            for c in dst_class:
                dst_class[dst_class.index(c)]['num_clusters'] = num_clusters
                dst_class[dst_class.index(c)]['distance'] = d
                result.append(c)
            class_z2(file_path, d, num_clusters, dst_png_path)
    save_dict_list_to_excel(result, dst_xls_path)


if __name__ == '__main__':
    src_file_path = 'result/step8.高频药物矩阵10.xlsx'
    class_z_final(src_file_path)

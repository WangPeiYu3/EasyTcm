import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
from upsetplot import plot  # 注意：这里我们直接从upsetplot导入plot函数，而不是UpSet类

def convert_to_multiindex(db):
    # 定义一个函数来检查每个项目是否存在于给定的列表中
    items_to_check = []
    item_count = []
    for r in db:
        for c in r:
            if c not in items_to_check:
                items_to_check.append(c)
                item_count.append(1)
            else:
                idx = items_to_check.index(c)
                item_count[idx] = item_count[idx] +1

    def check_presence(item_list, items_to_check):
        return [item in item_list for item in items_to_check]

    multi_index_values = [check_presence(item_list, items_to_check) for item_list in db]
    print(multi_index_values,item_count)
    dst = []
    dst_num = []
    for m in multi_index_values:
        if m not in dst:
            dst.append(m)
            dst_num.append(1)
        else:
            idx = dst.index(m)
            dst_num[idx] = dst_num[idx] + 1
    print(dst, dst_num)

    # 创建 MultiIndex
    index = pd.MultiIndex.from_tuples(dst, names=items_to_check)

    return index, dst_num

def draw_up_set(db,upset_png_name='upset_plot.png'):
    # 测试数据
    # 调用函数并打印结果
    index, data = convert_to_multiindex(db)
    # 将数据和索引组合成一个DataFrame
    df = pd.DataFrame({'value': data}, index=index)
    series = df['value']
    print(series)
    # 绘制UpSet图，设置显示交集大小，并指定图表背景颜色
    plot(series, show_counts=True, facecolor="green")
    # 添加图表标题



    # 保存图表为PDF文件
    plt.savefig(upset_png_name)
    # 显示图表（注意：在某些环境中，如Jupyter Notebook，这一步可能是可选的）


import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori


def find_frequent_itemsets(db):
    # 转换数据格式
    te = TransactionEncoder()
    te_ary = te.fit(db).transform(db)
    df = pd.DataFrame(te_ary, columns=te.columns_)

    # 计算最小支持度
    total_transactions = len(db)
    min_support_value = 2 / total_transactions

    # 应用Apriori算法
    frequent_itemsets = apriori(df, min_support=min_support_value, use_colnames=True)

    # 初始化空列表用于存储频繁项集
    fre = []

    # 按行处理频繁项集
    for index, row in frequent_itemsets.iterrows():
        itemset = list(row['itemsets'])
        count = round(row['support'] * total_transactions)

        # 只添加包含多于一个项目的频繁项集
        if len(itemset) > 1:
            fre.append({'itemset':itemset,'count':count})

    return fre


# 调用函数
if __name__ == '__main__':
    db = [['酸枣仁', '甘草', '大枣'],
          ['酸枣仁', '党参', '甘草'],
          ['酸枣仁', '党参', '大枣'],
          ['酸枣仁', '黄精', '甘草'],
          ['党参', '甘草', '大枣']]
    draw_up_set(db)
    result = find_frequent_itemsets(db)
    print(result)


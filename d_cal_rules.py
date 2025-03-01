from collections import defaultdict, Counter
from itertools import combinations



def generate_next_candidates(frequent_itemsets_by_size, k):
    """从频繁 (k-1) 项集中生成 k 项集候选"""
    candidates = []
    for i in range(len(frequent_itemsets_by_size[k - 2])):
        for j in range(i + 1, len(frequent_itemsets_by_size[k - 2])):
            # 前 k-2 项相同，最后一项不同的 (k-1) 项集可以合并成 k 项集
            itemset_i = list(frequent_itemsets_by_size[k - 2].keys())[i]
            itemset_j = list(frequent_itemsets_by_size[k - 2].keys())[j]
            if itemset_i[:k - 2] == itemset_j[:k - 2]:
                candidate = sorted(list(set(itemset_i) | set(itemset_j)))
                # 检查所有 (k-1) 子集是否都是频繁的
                if all(tuple(subset) in frequent_itemsets_by_size[k - 2] for subset in combinations(candidate, k - 1)):
                    candidates.append(candidate)
    return candidates


def find_frequent_itemsets(transactions, min_support):
    # 计算单项的支持度
    item_counts = Counter(item for transaction in transactions for item in transaction)
    frequent_items = {tuple([item]): count for item, count in item_counts.items() if
                      count / len(transactions) >= min_support}

    # 初始化频繁项集列表
    frequent_itemsets_by_size = [frequent_items]

    k = 2
    while True:
        # 生成下一层的候选项集
        candidates = generate_next_candidates(frequent_itemsets_by_size, k)

        # 如果没有新的候选项集，结束
        if not candidates:
            break

        # 计算候选项集的支持度
        candidate_counts = Counter()
        for transaction in transactions:
            for candidate in candidates:
                if all(item in transaction for item in candidate):
                    candidate_counts[tuple(candidate)] += 1

        # 筛选出频繁项集
        frequent_itemsets = {itemset: count for itemset, count in candidate_counts.items() if
                             count / len(transactions) >= min_support}

        if not frequent_itemsets:
            break

        frequent_itemsets_by_size.append(frequent_itemsets)
        k += 1

    # 合并所有大小的频繁项集
    all_frequent_itemsets = {itemset: count for layer in frequent_itemsets_by_size for itemset, count in layer.items()}

    return all_frequent_itemsets


def calculate_metrics(frequent_itemsets, transactions):
    num_transactions = len(transactions)
    rules = []

    for itemset, support_count in frequent_itemsets.items():
        for i in range(1, len(itemset)):
            for antecedent in combinations(itemset, i):
                consequent = tuple(sorted(set(itemset) - set(antecedent)))
                antecedent_count = frequent_itemsets.get(tuple(antecedent), 0)
                consequent_count = frequent_itemsets.get(consequent, 0)

                if antecedent_count > 0 and consequent_count > 0:
                    confidence = support_count / antecedent_count
                    lift = confidence / (consequent_count / num_transactions)
                    rule = {
                        'antecedent': antecedent,
                        'consequent': consequent,
                        'support': support_count / num_transactions,
                        'confidence': confidence,
                        'lift': lift
                    }
                    rules.append(rule)
    return rules

def calculate_rulues(src_files, fre_file_path='frequent_itemsets.xlsx',rules_file_path='rules.xlsx',col_names='处方S',min_support=0.8,min_confidence=0.8,min_lift=1):
    from a_med_stand import save_dict_list_to_excel,read_excel_to_dict_list
    transactions=[]
    dict_list = read_excel_to_dict_list(src_files)
    for dict_item in dict_list:
        dict_item_list = dict_item[col_names].split("、")
        transactions.append(dict_item_list)

    frequent_items =[]
    frequent_itemsets = find_frequent_itemsets(transactions, min_support)
    for key in frequent_itemsets.keys():
        dict_item = {}
        dict_item['项集'] = "、".join(list(key))
        dict_item['支持度'] = frequent_itemsets[key]
        if dict_item['项集'].count("、")>0:
            frequent_items.append(dict_item)
    save_dict_list_to_excel(frequent_items, fre_file_path)

    # 计算关联规则的指标
    rules = calculate_metrics(frequent_itemsets, transactions)

    dst_rules = []
    dst_rules_for_draw = []
    # 打印结果
    for rule in rules:
        dict_rule = {}
        dict_rule['前项'] = "、".join(list(rule['antecedent']))
        dict_rule['后项'] = "、".join(list(rule['consequent']))
        dict_rule['支持度百分比'] = round(rule['support'], 4)*100
        dict_rule['置信度百分比'] = round(rule['confidence'], 2)*100
        dict_rule['提升度'] = round(rule['lift'], 4)*100
        if dict_rule['置信度百分比'] > min_confidence*100 and dict_rule['提升度'] > min_lift:
            dst_rules.append(dict_rule)
            if dict_rule['前项'].count("、")==0 and dict_rule['后项'].count("、")==0:
                dst_rules_for_draw.append(dict_rule)
            print(dict_rule)
    save_dict_list_to_excel(dst_rules, rules_file_path)
    rules_file_path_for_draw = rules_file_path.replace(".xlsx", "_for_draw.xlsx")
    save_dict_list_to_excel(dst_rules_for_draw, rules_file_path_for_draw)


if __name__ == '__main__':

    calculate_rulues('step1.药物标准化后.xlsx',min_support=0.1,min_confidence=0.8,min_lift=1)

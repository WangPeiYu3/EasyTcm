import plotly.graph_objects as go


# 定义节点
node_labels = ['甘草', '桑葚', '大枣', '熟地']
# 定义边，即源节点、目标节点和权重
source = [0, 0, 1, 1, 2, 3]
target = [1, 2, 2, 3, 3, 0]
value = [4, 8, 10, 2, 8, 5]


# 创建链接字典
link_dict = dict(source=source, target=target, value=value)

# 创建节点字典
node_dict = dict(label=node_labels, pad=60, thickness=20)

# 创建和弦图
fig = go.Figure(data=[go.Sankey(node=node_dict, link=link_dict)])

# 更新布局
fig.update_layout(title_text="Basic Chord Diagram", font_size=10)

# 显示图形
fig.show()
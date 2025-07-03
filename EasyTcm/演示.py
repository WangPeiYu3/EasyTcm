import numpy as np
import plotly.graph_objects as go
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 模拟数据（假设有 10 个特征，每个特征 20 个样本值）
np.random.seed(42)
X = np.random.rand(20, 10)
feature_names = [f'Feature{i}' for i in range(1, 11)]

# PCA 分析
X_scaled = StandardScaler().fit_transform(X)
pca = PCA(n_components=3)
pca.fit(X_scaled)

# 获取前三个主成分载荷
x_loadings = pca.components_[0]
y_loadings = pca.components_[1]
z_loadings = pca.components_[2]

# 绘图
fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=x_loadings,
    y=y_loadings,
    z=z_loadings,
    mode='markers+text',
    marker=dict(
        size=8,
        color='royalblue',
        line=dict(color='black', width=1),
        opacity=0.8
    ),
    text=feature_names,
    textposition='top center',
    textfont=dict(size=12, color='darkred')
))

fig.update_layout(
    title='3D PCA Loadings Plot',
    scene=dict(
        xaxis_title='PC1',
        yaxis_title='PC2',
        zaxis_title='PC3',
        xaxis=dict(showbackground=True, backgroundcolor='white'),
        yaxis=dict(showbackground=True, backgroundcolor='white'),
        zaxis=dict(showbackground=True, backgroundcolor='white'),
        aspectmode='cube'
    ),
    margin=dict(l=10, r=10, t=40, b=10),
    template='simple_white',
    showlegend=False
)

# 设置视角更美观
fig.update_scenes(camera=dict(eye=dict(x=1.4, y=1.4, z=1.2)))

# 保存为 SVG 文件
fig.write_image("pca_example_output.svg", format="svg")

print("✅ SVG 图已保存为 'pca_example_output.svg'")

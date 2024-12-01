import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score


def get_best_params(data, param_grid=None, verbose=False):
    """获取 DBSCAN 的最佳参数"""
    # 如果没有初始化 param_grid
    if param_grid is None:
        param_grid = {
            'eps': [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
            'min_samples': [2, 4, 6, 8, 10, 12, 14]
        }

    # 创建 DBSCAN 实例
    dbscan = DBSCAN()

    # 手动进行网格搜索
    best_score = -1  # 用于存储最佳轮廓系数
    best_params = {}  # 用于存储最佳参数
    for eps in param_grid['eps']:
        for min_samples in param_grid['min_samples']:
            dbscan.set_params(eps=eps, min_samples=min_samples)
            labels = dbscan.fit_predict(data)

            # 计算轮廓系数
            if len(set(labels)) > 1:  # 确保至少有两个簇
                score = silhouette_score(data, labels)
                if verbose:
                    print(f"eps={eps}, min_samples={min_samples}, silhouette_score={score}")

                if score > best_score:
                    best_score = score
                    best_params = {'eps': eps, 'min_samples': min_samples}

    return best_params


def get_labels(data, best_params):
    """使用最优参数计算聚类标签"""

    dbscan = DBSCAN(**best_params)

    # 进行聚类
    dbscan.fit(data)

    # 获取聚类标签
    labels = dbscan.labels_

    return labels


def simple_scatter(data, labels, title='DBSCAN Clustering'):
    """绘制聚类结果"""

    # 绘制结果
    scatter = plt.scatter(data[:, 0], data[:, 1], c=labels, cmap='viridis')

    # 使用 set_unique_labels 来为不同的簇分配标签
    unique_labels = np.unique(labels)
    handles = [plt.Line2D([0], [0],
                          marker='o',
                          color='w',
                          markerfacecolor=scatter.cmap(i / len(unique_labels)),
                          markersize=10)
               for i in range(len(unique_labels))]
    labels_for_legend = [f'Cluster {label}' for label in unique_labels]
    plt.legend(handles, labels_for_legend, title="Clusters", loc='center left', bbox_to_anchor=(1, 0.5))

    plt.title(title)
    plt.show()


def auto_dbscan(data,
                param_grid=None,
                verbose=False,
                title='DBSCAN Clustering'):
    """"自动对参数进行寻优的 DBSCAN 算法"""
    # 获取最优参数
    best_params = get_best_params(data, param_grid, verbose)

    # 获取聚类标签
    labels = get_labels(data, best_params)

    # 绘制聚类结果
    simple_scatter(data, labels, title)

    return best_params, labels


def denstream_init(data,
                    decaying_factor=0.01,
                    beta=0.5,
                    mu=2.5,
                    epsilon=0.5,
                    n_samples_init=10):
    """DenStream 流式聚类初始化"""

    # 初始化 DenStream 聚类器
    denstream = cluster.DenStream(decaying_factor=decaying_factor,
                                  beta=beta,
                                  mu=mu,
                                  epsilon=epsilon,
                                  n_samples_init=n_samples_init)

    # 对数据流进行增量学习
    for x, _ in stream.iter_array(data):
        denstream.learn_one(x)

    return denstream

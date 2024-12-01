import numpy as np
from collections import deque

class MicroCluster:
    def __init__(self, point, timestamp):
        self.center = np.array(point)
        self.points = deque([point])
        self.last_update = timestamp
        self.weight = 1

    def update(self, point, timestamp):
        self.points.append(point)
        self.weight += 1
        self.center = ((self.weight - 1) * self.center + point) / self.weight
        self.last_update = timestamp

class DenStream:
    def __init__(self, epsilon=0.5, beta=0.2, lambd=0.01, min_points=3):
        self.epsilon = epsilon  # 半径范围内的距离
        self.beta = beta        # 微簇的最低权重阈值
        self.lambd = lambd      # 时间衰减速率
        self.min_points = min_points
        self.micro_clusters = []

    def _distance(self, point1, point2):
        return np.linalg.norm(np.array(point1) - np.array(point2))

    def _is_within_epsilon(self, cluster, point):
        return self._distance(cluster.center, point) <= self.epsilon

    def fit(self, point, timestamp):
        # 寻找距离 point 在 epsilon 范围内的微簇
        closest_cluster = None
        for cluster in self.micro_clusters:
            if self._is_within_epsilon(cluster, point):
                closest_cluster = cluster
                break

        # 如果找到了适合的微簇，更新它
        if closest_cluster:
            closest_cluster.update(point, timestamp)
        else:
            # 否则，创建一个新的微簇
            new_cluster = MicroCluster(point, timestamp)
            self.micro_clusters.append(new_cluster)

        # 时间衰减每个微簇的权重
        self._decay_micro_clusters(timestamp)

        # 删除权重低于阈值的微簇
        self._remove_weak_clusters()

    def _decay_micro_clusters(self, timestamp):
        for cluster in self.micro_clusters:
            delta_time = timestamp - cluster.last_update
            decay_factor = np.exp(-self.lambd * delta_time)
            cluster.weight *= decay_factor
            cluster.last_update = timestamp

    def _remove_weak_clusters(self):
        self.micro_clusters = [cluster for cluster in self.micro_clusters if cluster.weight >= self.beta]

    def get_clusters(self):
        return [cluster.center for cluster in self.micro_clusters]

# 测试最简版 DenStream 算法
denstream = DenStream(epsilon=1.0, beta=0.5, lambd=0.01)

# 模拟输入的数据流
stream_points = [
    (1.0, 2.0),
    (1.2, 2.1),
    (3.5, 4.0),
    (1.1, 2.2),
    (4.0, 3.8),
    (3.7, 4.1),
    (10.0, 10.0)  # 离群点
]

timestamps = range(len(stream_points))
for point, timestamp in zip(stream_points, timestamps):
    denstream.fit(point, timestamp)
    print(f"Clusters at time {timestamp}: {denstream.get_clusters()}")

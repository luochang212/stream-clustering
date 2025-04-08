# stream-clustering

> 直接说结论：全量聚类用 DBSCAN；无监督流式聚类用 DenStream；已知聚类数、按较大时间间隔获取聚类标签且对计算量敏感，用 CluStream.

本文涉及的内容包括：

- 提供 DBSCAN、DenStream 和 CluStream 三种聚类算法的使用示例
- 开发对 DBSCAN 自动调参并输出聚类标签的函数 [auto_dbscan](/utils.py#L76)
- 验证 DenStream 的推理结果（簇号）是否在学习过程中发生变化：会变
- DBSCAN、DenStream 和 CluStream 全量训练效果对比：DBSCAN 最好
- DenStream 和 CluStream 增量训练效果对比：DenStream 最好

✨ 注意：运行以下代码依赖 [utils.py](/utils.py) 文件。

### 一、DBSCAN

DBSCAN 是一种基于密度的聚类算法，用于从大量数据中识别出高密度区域并将其分为不同的簇。与传统的基于划分的聚类算法（如 K-means）不同，DBSCAN 不需要预先指定簇的数量，并且能够识别噪声数据和异常值。

1. DBSCAN 算法介绍
2. DBSCAN 的简单示例
3. DBSCAN 的可选参数
4. DBSCAN 自动调参：
    - 基于 K 距离图选择 `eps`
    - 选择 `min_samples` 的经验法则
    - 使用网格搜索结合合适的评估指标
5. 使用 `best_params` 进行聚类
6. 一站式 DBSCAN 函数


### 二、DenStream

DenStream 适合不知道具体的聚类数，且需要实时获取聚类标签的情况。

1. DenStream 算法介绍
2. DenStream 的简单示例
3. DenStream 的可选参数
4. 验证：推理结果是否随时间变化
5. DBSCAN 与 DenStream 效果对比
6. 使用 DBSCAN 优化过的 `epsilon` 参数


### 三、CluStream

CluStream 是一种需要明确指定聚类数的算法。它在一段时间内的聚类效果不错，也就是说，如果你的需求是有时间间隔的，比如每 10 分钟获取一次聚类结果，CluStream 的效果是可以接受的。

1. CluStream 算法介绍
2. CluStream 的简单示例
3. CluStream 的可选参数
4. CluStream 全量训练：
    - 宏簇数量 与 真实聚类数 相等的情况
    - 宏簇数量 与 真实聚类数 不等的情况
5. DenStream 与 CluStream 增量训练效果对比


### 四、附录：轮廓系数

轮廓系数是一种用于评估聚类效果的指标，它从单个样本的角度衡量其聚类的合理性。轮廓系数综合考虑了样本与其所属簇内点的相似性（紧密度）和样本与其最近簇的点的相似性（分离度）。


### 参考资料

- <a href="https://riverml.xyz/latest/api/cluster/DenStream/" target="_blank">DenStream</a>
- <a href="https://riverml.xyz/latest/api/cluster/CluStream/" target="_blank">CluStream</a>
- <a href="https://riverml.xyz/latest/api/cluster/DBSTREAM/" target="_blank">DBSTREAM</a>


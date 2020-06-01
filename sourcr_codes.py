# 导入所需要的包
import pandas as pd
import Levenshtein
from sklearn.cluster import KMeans

# 以列表形式保存商品名
data = []

# 打开文件，对每一行拆分为单独的商品名加入data中，注意去重
with open('basket_row.csv', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.rstrip(',\n')
        line = line.split(',')
        for meb in line:
            if meb not in data:
                data.append(meb)

# 转化为DataFrame对象
data_F = pd.DataFrame(data)
data_F.columns = ['shopname']

# 定义计算每一个商品与其他商品的编辑距离的函数
def calculate_compile_distance(shopname):
    distances = []
    for meb in data:
        distances.append(Levenshtein.distance(shopname,meb))
    return distances

# 计算编辑距离向量矩阵
for meb in data_F.shopname:
    data_F[meb] = calculate_compile_distance(meb)

# 提取向量矩阵
X = data_F.drop('shopname', axis = 1)

# 设置合理的簇数进行聚类
kmeans = KMeans(n_clusters=1900)
kmeans.fit(X)

# 将商品名与其类别标签整合
result = pd.DataFrame(data)
result['类别'] = kmeans.labels_

# 按照类别标签为key进行分桶，分到所属的簇中
result_dict = dict()
for line in result.itertuples():
    result_dict.setdefault(line[2],[]).append(line[1])

# 保存那些商品数量大于2的簇（即有不同的规格）
over_two = []
for key, value in result_dict.items():
    if len(value) > 1:
        over_two.append(value)

# 查看聚类结果
for line in over_two:
    print(line)
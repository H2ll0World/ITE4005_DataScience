# assignment 3
# DBSCAN
# import sklearn

# 이제 모듈을 가져올 수 있음
# import your_module
from sklearn.neighbors import RadiusNeighborsClassifier

# import sys
inputFile = sys.argv[1]
n = sys.argv[2]
eps = sys.argv[3] # 엡실론 : 반지름
minPtr = sys.argv[4] # 

inputF = open(inputFile, "r")
# outputF = open(outputFile, "w") # output file이 없네?

dataset = []
label = []
while True:
    # data : objectNum /t x_cordinate /t y_cordinate
    data = inputF.readline().split()
    if not data: break # 데이터가 더 이상 없는 경우 break
    dataset.append(data)
    label.append("")
    # for i in data:

radius = 2.0
rn = RadiusNeighbors(radius=eps)
rn.fit(data)
indices = rn.radius_neighbors(point, return_distance=False)
print(f"Indices of the neighbors within radius {radius}: {indices}")

# print(label)

# for p in dataset:
#     print(p)
#     # print(label[p])

# for i in range(len(dataset)):
#     data = dataset[i]
#     if(label)
import sys
import math

trainFile = sys.argv[1]
testFile = sys.argv[2]
resultFile = sys.argv[3]

train = open(trainFile, "r")
test = open(testFile,"r")
result = open(resultFile, "w")
# test = "5test"

feature = train.readline().split() # 리스트 자료형으로 반환 ['age', 'income', ... , 'class']

featureNum = len(feature) - 1 # 마지막은 class label 이므로
dataset = [] # 굳이 set으로 할 필요가? list로 해도 되는 것 아닌가?
# set으로 순서가 중요하지 않으므로 ?
# set의 각 원소는 list로 가능? 각 원소 내부의 순서는 중요함
dataIdx = 0
curData = set()
while True:
    temp = train.readline().split()
    if not temp: break
    curData.add(dataIdx)
    dataIdx += 1
    dataset.append(temp)

testList = [] # 순서를 유지해야 하므로
featureName = test.readline().split() #
while True:
    temp = test.readline().split()
    if not temp: break
    testList.append(temp)

# print(dataset)

# gain ratio
# ratio를 먼저 구해야 하나?

# GainRatio(A) = Gain(A) / SplitInfo(D)
    # Gain의 문제점을 개선한 방식
    # Gain(A) : Information gain : A로 나누기 전과 후의 entropy 차이
        # Gain(A) = Info(D) - Infoa(D)
        # Info(D) = -sigma(pi * log2(pi)) : before
        # Infoa(D) = sigma{(Dj/D) * Info(Dj)} : after
    # splitInfo(D) = -sigma{(Dj/D) * log2(Dj/D)}

# data 가 주어졌을 때의 info를 계산함
def calInfo(data): # data : set, {1, 2, 3} 이런 식으로 들어있음
    class_num = {} # dictionary 자료형
    for iter in data:
        label = dataset[iter][featureNum]
        # print(label)
        if label not in class_num:
            class_num[label] = 1
        else:
            class_num[label] += 1
    info = 0.0
    base = len(data)
    for value in class_num.values():
        pi = value / base
        info += -(pi * math.log2(pi))
    return info

# inputData = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13}
# print(f"info : {calInfo(inputData)}")

# recursion을 위해 따로 함수정의
    # 사용한 feature 값을 복사해서 넘겨줘야 함
    # data 값 set으로

# gain이 최대가 되는 feature의 번호를 리턴
# gain = info - infoa 이므로 infoa가 최소가 되면 됨
def calGain(usedFeature, data): # usedFeature : {1, 2, 3} 이런식으로 feature의 idx를 저장
    if len(usedFeature) == featureNum: # feature를 다 사용한 경우
        return -1
    
    maxGain = 0.0
    maxFeature = 0
    # Info먼저 계산
    info = calInfo(data) # 현재 데이터의 타입이 모두 같아도 종료해야 함
    if info == 0:
        return -2
    # print(f"info : {info}")
    maxGainRatio = 0.0

    # 마지막 feature는 class_label 이므로 사용X
    for iter in range(featureNum): # iter : 특정 feature를 나타냄
        # 부모에서 이미 사용한 feature이면 넘어감
        if iter in usedFeature:
            continue
        # print(f"feature num : {iter}")
        infoa = 0.0
        splitInfo = 0.0
        # 데이터를 해당 feature(iter)에 따라 분류 # class label이 2개 이상일 수 도 있음
        multimap = {} # c의 multimap과 같은 자료구조를 사용하기 위해서 dictionary의 element가 set이야됨 : calInfo를 사용하기 위해
        for dataIter in data:
            curDataFeature = dataset[dataIter][iter]
            if curDataFeature not in multimap:
                multimap[curDataFeature] = set()
            multimap[curDataFeature].add(dataIter)

        # multimap은 해당 feature에 따라서 분류되어 있음
        for values in multimap.values(): # values는 set임
            infoDj = calInfo(values)
            infoa += (len(values)/len(data) * infoDj)
            sTemp = len(values)/len(data)
            splitInfo += -(sTemp * math.log2(sTemp))
        # print(f"in feature {iter} : infoa : {infoa}, splitInfo : {splitInfo}")
        curGainRatio = (info - infoa) / splitInfo
        # print(f"curGainRatio : {curGainRatio}")
        # print("")
        if curGainRatio > maxGainRatio:
            maxGainRatio = curGainRatio
            maxFeature = iter
    return maxFeature

# print(f"calGain : {calGain({}, {0,1,2,3,4,5,6,7,8,9,10,11,12,13})}")
class Node:
    def __init__(self, featureNum : int, isLeaf : bool, class_label):
        self.featureNum = featureNum # 이 노드에서 사용할 feature의 번호
        self.children = {} # feature : 해당 자식노드
        self.isLeaf = isLeaf
        self.class_label = class_label
        # self.curIdx = 

nextNode = 1; # 다음에 생성할 노드의 번호
rootNode = Node(0, False, "")
nodeList = [rootNode]

# 가장 많은 class_label을 return
def majorityVoting(data : set):
    result = {}
    for iter in data:
        class_label = dataset[iter][featureNum]
        if class_label not in result:
            result[class_label] = 1
        else:
            result[class_label] += 1
    # 가장 많은 class_label을 return
    maxNum = 0
    maxFeature = ""
    for key, value in result.items():
        if value > maxNum:
            maxNum = value
            maxFeature = key
    return maxFeature

# root부터 시작해서 재귀적으로
def recursion(usedFeature : set, data : set, curNode : int): # 부모에서 자식을 생성해야 함
    # print("----------------------------------------------------------------------")
    # print(f"curNode : {curNode}, usedFeature : {usedFeature}, data : {data}")
    curFeatureIdx = calGain(usedFeature, data)
    nodeList[curNode].featureNum = curFeatureIdx
    
    # 이떄 leaf 즉 decision을 해아함 이에 대한 처리 추가
    if curFeatureIdx == -1 or curFeatureIdx == -2: # feature를 다 사용한 경우 or # data의 feature가 1가지인 경우
        # majority voting을 해야함
        nodeList[curNode].isLeaf = True
        nodeList[curNode].class_label = majorityVoting(data)
        # print(f"LeafNode : {curNode}, class_label : {nodeList[curNode].class_label}")
        return
    usedFeature.add(curFeatureIdx)
    # 선택된 feature를 기준으로 data를 나눠줘야 함
    data_div = {} # dictionary 안에 element는 
    for iter in data:
        curFeature = dataset[iter][curFeatureIdx]
        if curFeature not in data_div:
            data_div[curFeature] = set()
        data_div[curFeature].add(iter)
    global nextNode
    for key, valus in data_div.items():
        newNode = Node(-1, False, majorityVoting(valus))
        nodeList.append(newNode) # 이게 nexNode idx를 가짐
        nodeList[curNode].children[key] = nextNode
        # print(f"curNode : {curNode}, featureNum : {curFeatureIdx}")
        # print(f"curNodeIdx : {curNode}, childNodeIdx : {nextNode}, toFeature : {key}\n")
        nextNode += 1
        copy_set = set(usedFeature)
        recursion(copy_set, valus, nextNode - 1)
        

usedFeature = set()
recursion(usedFeature, curData, 0) # curData : {0, 1, 2, 3, ... }

# root부터 시작해서 내려감
def test(testTuple : list, curNodeIdx : int):
    curNode = nodeList[curNodeIdx]
    # print(f"curNodeIdx : {curNodeIdx}")
    if curNode.isLeaf:
        # print(f"leafNode, class_label : {curNode.class_label}")
        return curNode.class_label
    feature = testTuple[curNode.featureNum]
    # print(f"in test : feature : {feature}\n")
    if feature not in curNode.children:
        # print(f"exception : curNode : {curNodeIdx}, clss : {curNode.class_label}")
        return curNode.class_label
    nextNodeIdx = curNode.children[feature]
    return test(testTuple, nextNodeIdx)

def printResult(testList : list):
    result.write("\t".join(str(x) for x in feature))
    print("\t".join(str(x) for x in feature))
    result.write("\n")
    
    for i in testList:
        label = test(i, 0)
        result.write("\t".join(str(x) for x in i) + f"\t{label}\n")
        # print("\t".join(str(x) for x in i) + f"\t{label}")

# print("\n --------------- test ---------------")
printResult(testList)
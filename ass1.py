# assingment 1
# Apriori algorithm을 사용해서 association rule을 찾는 것

# Apriori algoruthm : infrequent 한 itemset이 있다면, superset도 infrequent하다
# 1 - itemset을 스캔
# 반복하는 것
    # k + 1 - generate candidate
    # k + 1 - pruning before count
    # k + 1 - pruning after count(not frequent를 terminate)

import sys

# 

min_sup = int(sys.argv[1])
inputFile = sys.argv[2]
outputFile = sys.argv[3]

# print(f"min_sup : {min_sup}") # %네
inputF = open(inputFile, "r")
outputF = open(outputFile, 'w')
# with open(outputF, 'w') as file:
    # print(f"Name: {name}, Age: {age}", file=file)

# first case
c1 = {} # candidiate 1 # dictionary
# 왜 만든것? => supportHash는 dictionary 자료형이므로 탐색이 불가능 해서 따로 만듬
largeList = [] # element는 list element의 element는 set
transactions = [] # element는 set
supportHash = {}
notL = []

while True:
    items = inputF.readline().split() # [item_id]\t[item_id]\t[item_id]\t

    # items = items.split()
    t_set = set()
    if not items: break
    for i in items:
        t_set.add(int(i))
        try:
            c1[i] = c1[i] + 1
        except KeyError: # 해당 키 값이 없는 경우
            c1[i] = 1
    transactions.append(t_set)

t_list = [] # frequent
t_n_list = [] # not frequent
# cnt_list = []
# t_cnt_list = set()
for key, value in c1.items():
    #print(f"key : {key}, value : {value}")
    if (value / len(transactions)) * 100 >= min_sup:
        t_set = {int(key)} # set
        t_list.append(t_set)
        # t_cnt_list.append(value)
        # print(f"key : {tuple(key)}")
        t_s = set()
        t_s.add(int(key))
        t_s = list(t_s)
        t_s.sort()
        supportHash[tuple(t_s)] = int(value)
    else:
        t_set = {int(key)}
        t_n_list.append(t_set)

# supportList.append(t_cnt_list)
t_list.sort()
largeList.append(t_list)
# print(f"test1.00 : largeList : {largeList}") # 여기까진 문제X
notL.append(t_n_list)
# print(f"largeList : {largeList}")
# print(f"transactions : {transactions}")

# Apriori Algorithm
stage = 1
while True: # 종료조건은 어떻게?
    stage = stage + 1
    # print(f"stage : {stage}")
    # pruning before candidate generation
        # to do this we need to store deleted transaction
        # actually after generation before counting
        # except l1 to c2 stage

    # candidate generation
    # self joining
    candidate = set() # list # element is set
    # print("before for loop")
    for i in largeList[stage - 2]:
        # print("in for loop1")
        for j in largeList[stage - 2]:
            # print("in for loop2")
            t_candidate = list(i.union(j)) # 합집한
            t_candidate.sort()
            # print(f"t_candidate : {t_candidate}")
            if len(t_candidate) == stage:
                candidate.add(tuple(t_candidate))
    # print(f"len : {len(candidate)}")
    if len(candidate) == 0: break
    # print(f"candidate : {candidate}") # 중복을 제거해야 함


    # pruning before candidate generation 
        # acutally after candidate gengeration 
        # before db counting
    # print(f"notL : {notL[stage - 2]}")
    # print(f"test candidate : {candidate}")
    candidate_before = [] # 이전에 제거된 것들을 빼주는 과정
    for i in candidate:
        isPossible = True
        for j in notL[stage - 2]:
            # print(f"set(i).intersection(set(j)) : {set(i).intersection(set(j))}")
            if len(set(i).intersection(set(j))) == stage - 1: # non intersection
                isPossible = False
        if isPossible: 
            # print(f"i : {i}")
            candidate_before.append(i)

    # print(f"test 1.01 candi_before : {candidate_before}")

    # print(f"candidate_before : {candidate_before}")
    # largeList.append(candidate_before) # 여기서 넣지 말고 테스트해서 넣기
    # break

    # pruning after candidate generation
        # need db scan
        # use dictionary to count
    candidate_cnt = {} # dictionary
    for i in transactions:
        for j in candidate_before: # candidate_before는 뭐지?
            # print(f"i : {i}")
            # print(f"j : {set(j)}")
            # print(f"i.intersection(set(j)) : {i.intersection(set(j))}")
            if len(i.intersection(set(j))) == stage:
                # dictionary's key is only immutable type
                set_to_tuple = tuple(j)
                try: 
                    candidate_cnt[set_to_tuple] = candidate_cnt[set_to_tuple] + 1
                except KeyError:
                    candidate_cnt[set_to_tuple] = 1
    # print(f"test 1.1 candidate_cnt : {candidate_cnt}")
    t_list = []
    t_cnt_list = []
    t_n_list = []
    # print(f"candidate_cnt : {candidate_cnt}")
    for key, value in candidate_cnt.items():
        # print(f"key : {key}, value : {value}")
        if (value / len(transactions)) * 100 >= min_sup:

            t_cnt_list.append(value)
            key = list(key)
            key.sort()
            t_list.append(set(key))
            supportHash[tuple(key)] = value
        else:
            t_n_list.append(set(key))
    

    if len(t_list) == 0: 
        # print("len(t_list) == 0")
        break
    # supportList.append(t_cnt_list)
    t_list.sort()
    # print(f"in apriori/ t_list : {t_list}") 
    largeList.append(t_list)
    # print(f"in apriori/ largeList : {largeList}")
    notL.append(t_n_list)


# print(f"largeList : {largeList}") # frequent list
# 값이 중볻되게 나오는 문제
# print(f"support: {supportHash}")
# int, int, list, list
def rec(cur, l, tmp, origin): # cur : 현재위치, l, 전체 길이, tmp : 현재 갖고있는 원소 , origin 원래의 배열
    # print(f"cur : {cur}, l : {l}, tmp : {tmp}, origin : {origin}")
    if cur == l: # 종료 조건 
        if(len(tmp) == 0 or len(tmp) == l): return
        # assoc : assoication rule
        assoc = set(origin) - set(tmp)
        # print(f"origin keyError : {origin}")
        # print(f"origin keyError : {set(origin)}")
        origin.sort()
        sup = supportHash[tuple(origin)] / len(transactions) * 100
        
        
        # if(len(tmp) == 1):
        #     tmp = tmp[0]
        #     sup_tmp = supportHash[tmp]
        #     tmp = {tmp}
        #     # print(f"tmp : {tmp}")
        # else:
        #     # tmp는 list => sort해주면 됨
        #     tmp = tuple(tmp)
        #     sup_tmp = supportHash[tmp] # key가 없는 경우 예외 처리
        #     tmp = set(tmp)
            # try:
                
            # except: # 예외가 발생하면 안되는 거 아님?
                # key가 없는 경우

        # if(len(assoc) == 1):
            # assoc = list(assoc)
        # else:
            # assoc = tuple(assoc)
        tmp.sort()
        sup_tmp = supportHash[tuple(tmp)]
        assoc = list(assoc)
        assoc.sort()
        assoc = tuple(assoc)
        # outputF.write(f"assoc : {assoc}\n")
        # assoc = tuple(assoc)
        origin.sort()
        conf = supportHash[tuple(origin)] / sup_tmp * 100
        r_sup = "{:.2f}".format(sup) # 이거 반올림 아니면 소수점2자리만?
        r_conf = "{:.2f}".format(conf) 
        # print(f"{set(tmp)}\t{set(assoc)}\t{r_sup}\t{r_conf}")
        # outputF.write(f"{set(tmp)} \t{set(assoc)} \t{r_sup} \t{r_conf}\n")
        outputF.write("{")
        for i in tmp:
            outputF.write(f"{i}")
            if i != tmp[len(tmp) - 1]:
                outputF.write(", ")
        outputF.write("}")
        # outputF.write("")
        outputF.write("\t{")
        for i in assoc:
            outputF.write(f"{i}")
            if i != assoc[len(assoc) - 1]:
                outputF.write(", ")
        outputF.write("}")
        # outputF.write("")
        outputF.write(f"\t{r_sup} \t{r_conf}\n")
        # outputF.write(f"{list(set(tmp))}\t{list(set(assoc))}\t{r_sup}\t{r_conf}\n")

        # 이건 왜 있는 거?
        # conf = supportHash[assoc] / supportHash[tuple(origin)] * 100
        # print(f"{tmp}\t{assoc}\t{sup}\t{conf}")
        return
    tmp1 = tmp[:]
    rec(cur + 1, l, tmp1, origin)
    # print(f"origin[cur] : {origin[cur]}")
    # tmp.add(int(origin[cur]))
    # tmp.append
    tmp2 = tmp[:]
    tmp2.append(origin[cur]) # 왜 해주는 거?
    # print(f"origin[cur] : {origin[cur]}")
    # print("test")
    rec(cur + 1, l, tmp2, origin)

isFirst = True
# print("testtest")
# print(f"largeList : {largeList}") # largeList에 중복된 값들이 들어가 있어서 rec에서 중복된 값들이 나옴
# print(f"{}")
for i in largeList:
    if isFirst:
        isFirst = False
        continue
    for j in i:
        # print(f"j : {j}")
        # origin이 정렬되지 않은 상태로 들어가서 [1, 2]와 [2, 1] 이 달라지는 문제
        j = list(j)
        j.sort()
        rec(0, len(j), list(), j)


        # for k in range(len(j)):

        # for k in j:
            # print(k)

        # j 를 2개로 나눠야 함
        



# print(items)
outputF.close()
inputF.close()
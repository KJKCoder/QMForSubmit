from collections import defaultdict
import copy

# dict에 원소가 존재하는지, While 루프 제어용
def checkDict(dict):
    for i in dict :
        for l in dict[i] :
            return True
    return False

#해밍 디스턴스 개수 세기
def countHD(x,y):
    count=0
    for i in range(0,len(x)):
        if x[i] != y[i] : count += 1  
    return count

#Minterm의 Binary형의 1의 개수 세기
def countOne(Binary):
    count = 0
    for i in Binary :
        if i == '1' :
            count += 1 
    return count

#2개의 민텀 옵티마이즈 (2로 통합)
def optimize2Minterm(x, y):
    NumOfVar = len(x)
    for i in range(0, NumOfVar):
        if x[i] != y[i]:
            return x[:i] + '2' + x[i+1:]
    return -1


#dict의 Value들을 하나의 Set으로 합치기
def combineValue(dict):
    result = set()
    for i in dict :
        for l in dict[i] :
            result.add(l)
    return result

#EPI 선별
def MakeEPI(PI) :
    EPI = set()
    
    for i in combineValue(PI) :
        count = 0
        temp = -1
        for x in PI :
            if i in PI[x] : count += 1 ; temp = x
            if count > 1 : temp = -1 ; break
        if(temp != -1) : EPI.add(temp)

    EPI = sorted(EPI)
    return EPI

# PI에서 EPI제거 (NEPI를 리턴)
def removeEPIonPI(PI, EPI) :
    for epi in EPI :
        PI.pop(epi)
    return PI

def makePI(minterm) :
    PI = {}
    answer = []
    
    NumOfVar = minterm[0] 
    NumOfMin = minterm[1] 
    
    tempArray = []
    for i in range(2, minterm[1] + 2):
        tempArray.append(str(bin(minterm[i])[2:]).zfill(NumOfVar))

    HammingDic = defaultdict(dict)
    SubHammingDic = defaultdict(dict)
    NullDict = defaultdict(dict)
    for i in range(0, NumOfVar + 2) :
        HammingDic[i] = {}
        SubHammingDic[i] = {}
        NullDict[i] = {}
    
    for i in range(0, len(tempArray)) :
        HammingDic[countOne(tempArray[i])][tempArray[i]] = [0,minterm[i+2]]

    while(checkDict(HammingDic)):
        for i in range(1, NumOfVar + 2) :
            for l in HammingDic[i-1] :
                for x in HammingDic[i] :
                    if countHD(l,x) == 1 : 
                        Optimized = optimize2Minterm(l,x)
                        SubHammingDic[countOne(Optimized)][Optimized] = [0]

                        SubHammingDic[countOne(Optimized)][Optimized].extend(HammingDic[i-1][l][1:])
                        SubHammingDic[countOne(Optimized)][Optimized].extend(HammingDic[i][x][1:])

                        HammingDic[i-1][l][0] = 1
                        HammingDic[i][x][0] = 1


        for i in HammingDic :
            for l in HammingDic[i] :
                if HammingDic[i][l][0] == 0 :
                    answer.append(l)
                    PI[l] = HammingDic[i][l][1:]

        HammingDic = copy.deepcopy(SubHammingDic)
        SubHammingDic = copy.deepcopy(NullDict)

    answer = sorted(answer)
    for i in range(0, len(answer)):
        answer[i] = answer[i].replace('2','-')

    return PI
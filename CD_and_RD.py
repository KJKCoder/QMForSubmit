from collections import defaultdict
import copy

#dict의 Value들을 하나의 Set으로 합치기
def combineValue(dict):
    result = set()
    for i in dict :
        for l in dict[i] :
            result.add(l)
    return result

# dict에서 Key와 Value를 서로 전환.  
def reversePIandMT(PI) :
    minterm = combineValue(PI)
    reversedPI = defaultdict(list)

    for cur in minterm :
        for pi in PI :
            if(cur in PI[pi]) : reversedPI[cur].append(pi) ; continue

    return reversedPI


#List안에 다른 List의 원소들이 모두 포함되는지 확인
def checkListInList(list1, list2):
    for i in list1 :
        if(not(i in list2)) : return 0
    return 1

# Column Dominance 적용 
def applyCD(PI) :

    #Dict의 Key를 PI에서 Minterm으로 전환
    reversedMT = reversePIandMT(PI)
    
    resultMT = reversedMT.copy()
    print("Before CD reversed: ", resultMT)
    for i in reversedMT :
        for l in reversedMT :
            # 특정 Minterm을 cover하는 PI이 다른 Minterm을 cover하는 PI에 포함 여부 확인 
            if(checkListInList(reversedMT[i], reversedMT[l])==1 and i != l) : 
                if(l in resultMT) :
                    resultMT.pop(l)
    print("After CD reversed: ", resultMT)
    
    return reversePIandMT(resultMT)

# Row Dominance 적용
def applyRD(PI) :
    resultPI = PI.copy()

    for i in PI :
        for l in PI :
            if(checkListInList(PI[i], PI[l])==1 and i != l) : 
                if(i in resultPI) :
                    resultPI.pop(i)

    return resultPI
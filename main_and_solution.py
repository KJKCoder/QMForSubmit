from collections import defaultdict
import copy
import PI_and_EPI as PNE
import CD_and_RD as Dom
'''
논리회로설계 20180539 김준관 도전과제 CD, RD 제출
'''
# 솔루션, While루프 + PM 여부
def solution(minterm):

    #Minterm PI로 최적화 후 출력
    PI = PNE.makePI(minterm)
    print("PI: ", PI)

    print("------------------------------------------------")
    checkFirst = 0
    EPI = []
    AllSelectedPI = [] #루프마다 생기는 Selected PI를 모으는 리스트
    NeedPM = True # Petrick Method를 적용할 필요가 있는지 없는지 확인
    

    while(True) :
        # 무한 루프 시작
        print(); print("Loop Start"); print()
        print("PI: ", PI)

        SelectedPI = PNE.MakeEPI(PI)
        
        # 처음 실행할 때 Selected PI는 EPI
        if(checkFirst == 0) : EPI = SelectedPI ; checkFirst = 1 ; print("EPI: ",EPI)
        else : AllSelectedPI.extend(SelectedPI) ; print("New Selected PI: ",SelectedPI)

        # NEPI PI에서 Selected PI 제거
        NEPI = PNE.removeEPIonPI(PI,SelectedPI)
        print("NEPI: ",NEPI)

        # NEPI가 없다면 종료
        if(len(NEPI) == 0) : NeedPM = False ; break
        
        # Column Dominance 적용
        print(); print("Column Dominance"); print()
        NEPI = Dom.applyCD(NEPI)
        print("After CD: ",NEPI)

        # Row Dominance 적용
        print(); print("Row Dominance"); print()
        print("Before RD: ",NEPI)
        NEPI = Dom.applyRD(NEPI)
        print("After RD: ",NEPI)
        
        # CD, RD 적용 후에도 PI 변화 없을 시 종료
        if(len(PI) == len(NEPI) and len(Dom.reversePIandMT(PI)) == len(Dom.reversePIandMT(NEPI))) : break

        PI = NEPI

    # NEPI가 남아있고 CD와 RD 둘 다 적용 불가능 할 경우
    print()
    if(NeedPM == True) : print("Need Petrick's Method")
    else : print("Finish(Not need Petrick's Method)")

    # 정렬 후 '2'를 '-'로 replace 하는 과정
    answer = []
    sorted(PI) ; sorted(AllSelectedPI)

    answer.extend(PI)
    answer.append("Selected PI")
    answer.extend(AllSelectedPI)
    answer.append("EPI")
    answer.extend(EPI)

    for i in range(0, len(answer)):
        answer[i] = answer[i].replace('2','-')

    print("------------------------------------------------")
    return answer




# main-----------------------------------------------------------------------------


minterm = [4, 8, 0, 4, 8, 10, 11, 12, 13, 15] 
#minterm = [3, 6, 0, 1, 2, 5, 6, 7] 
#minterm =  [6, 15, 0, 1, 2, 4, 5, 7, 10, 14, 18, 20, 25, 28, 30, 60, 61]
#minterm =  [7, 16, 0, 8, 10, 11, 12, 13, 17, 19, 20, 25, 29, 50 , 52, 60, 80, 90] 

ANSWER = solution(minterm)
print(); print("Answer")
print(ANSWER)

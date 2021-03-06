import pandas as pd
import itertools


## PreProces

file1 = open('/home/salusmoon/Desktop/ws/webMining/Transactions.txt', 'r')
Lines = file1.readlines()

count = 0
# Strips the newline character
data=[]
for line in Lines:
    count += 1
    array = line.split(",")
    data.append(array[:-1])


df = pd.DataFrame(data)



def createC1(dataSet):
    C1 = []
    for i in range(len(dataSet)):
        transaction= dataSet.loc[i]
        for item in transaction:
            if item!= None:
                if not [item] in C1:
                    C1.append([item])
                        
    C1.sort()
    return list(map(frozenset, C1))#use frozen set so we
                            #can use it as a key in a dict    


def scanD(D, Ck, minSupport):
    ssCnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                if not can in ssCnt: ssCnt[can]=1
                else: ssCnt[can] += 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support >= minSupport:
            retList.insert(0,key)
        supportData[key] = support
    return retList, supportData




def aprioriGen(Lk, k): #creates Ck
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk): 
            L1 = list(Lk[i])[:k-2]; L2 = list(Lk[j])[:k-2]
            L1.sort(); L2.sort()
            if L1==L2: #if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j]) #set union
    return retList




def apriori(dataSet, minSupport):
    C1 = createC1(dataSet)
    D = list(map(set, dataSet.values))
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while (len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)#scan DB to get Lk
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData






def generateRules(L, supportData, minConf):  #supportData is a dict coming from scanD
    bigRuleList = []
    for i in range(1, len(L)):#only get the sets with two or more items
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList    


def calcConf(freqSet, H, supportData, brl, minConf):
    prunedH = [] #create new list to return
    out= open("output.txt", "w")
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet-conseq] #calc confidence
        if conf >= minConf: 
            print (freqSet-conseq,'-->',conseq,'conf:',conf)
            brl.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    for i in range(len(brl)):
        out.write(str(brl[i][0]) +' --> '+ str(brl[i][1]) +' conf: '+str(brl[i][2]))
        out.write("\n")
    return prunedH

def rulesFromConseq(freqSet, H, supportData, brl, minConf):
    m = len(H[0])
    if (len(freqSet) > (m + 1)): #try further merging
        Hmp1 = aprioriGen(H, m+1)#create Hm+1 new candidates
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):    #need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)



L,suppData = apriori(df,0.005)
rules= generateRules(L,suppData, minConf=0.005)



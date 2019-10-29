import itertools
import json
import os
import numpy as np
import pandas as pd
import timeit
import mlxtend.frequent_patterns as mlx
folderPath = os.getcwd()
slash = '/'

def getApriori(list1,minsup):

    def checkPrune(subset,pruneListSetsPrec):
        for el in pruneListSetsPrec:
            if el <= subset:
                return True
        
        return False

    s = set()
    annotationListSets=[]
    for el in list1:
        setEl=set(el)
        s = s | setEl
        annotationListSets.append(setEl)
    
    sizeAnnotations = len(annotationListSets)
    aprioriList = []
    maxCardinality=len(s)
    pruneListSetsPrec=[]
    for L in range(1, maxCardinality+1):
        pruneSet=s
        s=set()
        pruneListSets=[]
        for subset in itertools.combinations(pruneSet, L):
            subset2 = set(subset)
            if checkPrune(subset2,pruneListSetsPrec):
                continue
            dictSubSet = {}
            dictSubSet[subset]=0
            for el in annotationListSets:
                if subset2 <= el:
                    dictSubSet[subset] += 1
            if dictSubSet[subset]/sizeAnnotations >= minsup:
                s = s | subset2
                aprioriList.append(dictSubSet)
            else:
                pruneListSets.append(subset2)
        
        pruneListSetsPrec=pruneListSets
        if len(s)==0:
            print (f'Break executed. Max cardinality:{maxCardinality}\tMax pruned cardinality:{L-1}')
            break
    return aprioriList,list(s)

 

def getBinaryMatrix(annotationSet,annotationList):
    columnMapping={}
    for index,value in enumerate(annotationSet):
        columnMapping[value]=index

    binaryMatrix=np.zeros((len(annotationList),len(annotationSet)))

    row=0
    for transactionItems in annotationList:
        for item in set(transactionItems):
            binaryMatrix[row][columnMapping[item]]+=1
        row+=1

    return binaryMatrix


print('1.\n Apriori implemented\n')

#2.
with open(folderPath + slash + 'modified_coco.json') as cocoFile:
    cocoJson=json.load(cocoFile)

coco=[]
annotationList=[]
for dictLine in cocoJson:
    annotationList.append(dictLine['annotations'])
    coco.append(dictLine)

print('2.\nFile succesfully red.\n')

#3.

minsup=0.02
"""
apriori,annotationIndexMapping=getApriori(annotationList,minsup)
print('3.\nCoco apriori:')

for line in apriori:
    for k,v in line.items():
        print(f'{k} -> {v}')
print(f'Number of frequent subset(My apriori algorithm):{len(apriori)}')"""
#4.
annotationSet=set()
for el in annotationList:
    annotationSet = annotationSet | set(el)
binaryMatrix=getBinaryMatrix(annotationSet,annotationList)
df = pd.DataFrame(data=binaryMatrix,columns=annotationSet)
#print(mlx.apriori(df,minsup))

#5.
print(f'Seconds to compute my apriori algorithm:{timeit.timeit(lambda: getApriori(annotationList,minsup),number=1):.3f}')
print(f'Seconds to compute mlxtend apriori algorithm:{timeit.timeit(lambda: mlx.apriori(df,minsup),number=1):.3f}')


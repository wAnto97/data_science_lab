from itertools import combinations
import json
import pandas as pd
from mlxtend.frequent_patterns import apriori
import timeit

toy_dataset = [['a','b'], ['b','c','d'], ['a','c','d','e'], ['a','d','e'], ['a','b','c'], ['a','b','c','d'], ['b','c'], ['a','b','c'], ['a','b','d'], ['b','c','e']]


def isSublist(first, second):

    if(type(first) != type(second)):
        if not second.__contains__(first):
            return False
    else:     
        for el in first:
            if not second.__contains__(el):
                return False

    return True

def support_calc(itemset_list, dataset, minsup):
    support_list = []
    #Con una lista di itemset della stessa cardinalità
    for itemset in itemset_list:
        support = 0
        for i in dataset:
            if(isSublist(itemset,i)):
                support += 1
    #Se il supporto è accettabile, lo metto nella mappa per il prossimo passo
        if(support/len(dataset) >= minsup):
            support_list.append(itemset)

    return support_list
                   

def first_step(dataset):
    elements = []
    for itemset in dataset: #Concateno le liste
        elements += itemset
    return list(set(elements)) #Sorted ha senso solo per il toy example


def second_step(dataset):
    return list(map(lambda x : sorted(list(x)), list(combinations(dataset,2))))


def list_from_prefix(prev_step,k):
    list_no_pruning = []
    for el in prev_step:
        prefix = el[0:k-2]
        for merge_el in prev_step:
            if(isSublist(prefix,merge_el)):
                itemset = sorted(set(el + merge_el))
                if(len(itemset) == k and itemset not in list_no_pruning):
                    list_no_pruning.append(itemset)
                 
    
    return list_no_pruning

def prune_list(curr_step, prev_step, k):

    for cs in curr_step:
        comb = list(map(lambda x : sorted(list(x)), list(combinations(cs,k-1))))
        if not isSublist(comb,prev_step):
            curr_step.remove(cs)          
            
    return curr_step

def k_th_step(prev_step, dataset, k):
    list_no_pruning = list_from_prefix(prev_step,k)
    step_k = prune_list(list_no_pruning, prev_step, k)
    return step_k

def matrix_trans(dataset, things):
    matrix = []

    for el in dataset:
        temp_vett = [0]*len(things)
        for thing in el:
            thing_index = things.index(thing)
            temp_vett[thing_index] = 1
        
        matrix.append(temp_vett)

    df = pd.DataFrame(data=matrix, columns=things)

    return df

def myApriori(dataset, minsup):
    steps = []
    things = first_step(dataset) #Creo il set dei miei items
    step1 = support_calc(things, dataset, minsup)
    # print("Length of step 1: " + str(len(step1_mod)))
    step2 = second_step(step1) #Creo le combinazioni a due a due
    step2 = support_calc(step2, dataset, minsup)
    # print("Length of step 2: " + str(len(step2)))
    steps.append(step1)
    steps.append(step2)

    #Adesso posso generalizzare per qualsiasi cardinalità k il ragionamento
    prev_step = step2
    for k in range(3,len(step1)):
        step_k = k_th_step(prev_step, dataset, k)  #Lista già 'pruned'
        step_k = support_calc(step_k, dataset, minsup)
        steps.append(step_k)
        prev_step = step_k
        # print("Length of step " + str(k) + " : " + str(len(prev_step)))

    return things,steps
        


with open("/home/anto/Scrivania/Python_Environment/datasets/modified_coco.json") as f:
    dataset = json.load(f)
    dataset = list(map(lambda x: list(x['annotations']), dataset))


#Normal execution
# my_apriori = myApriori(dataset, 0.02)
# things = my_apriori[0]
# my_result = my_apriori[1]
# df = matrix_trans(dataset,things)
# fi = apriori(df, 0.02)

# for step in my_result:
#     if(len(step) > 0):
#         for ass in step:
#             print(ass)
#         print("Length : " + str(len(step)))

# print(fi.to_string())
        

#Evaluating time
things = first_step(dataset)
df = matrix_trans(dataset,things)
print("My apriori lasts in : " + str(timeit.timeit(lambda: myApriori(dataset, 0.02), number=1)))
print("Library apriori lasts in : " + str(timeit.timeit(lambda: apriori(df, 0.02), number=1)))

import csv
import pandas as pd
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules


def map_for_trans(transaction_row):
    enum_transaction = ['invoice_no', 'stock_code', 'description', 'quantity', 'invoice_date', 'unit_price', 'customer_id', 'country']
    temp_map = {}
    
    for index,el in enumerate(transaction_row):
        temp_map[enum_transaction[index]] = el
    
    return temp_map


def groupby_tid(transactions):
    grouping_map = {}
    for row in transactions:
        if(row['invoice_no'] not in grouping_map.keys()):
            grouping_map[row['invoice_no']] = []
        
        grouping_map[row['invoice_no']].append(row['description'])

    return grouping_map


def create_lists(map_gb_tid):

    product_list = []
    transactions_list = []

    for trans in map_gb_tid.values(): #Concateno le liste per averne una con i prodotti
        product_list += trans
    
    transactions_list = list(map_gb_tid.keys())
    product_list = list(set(product_list)) #tolgo i duplicati

    return (transactions_list, product_list)


def matrix_trans(map_gb_tid):
    product_list = []
    matrix = []

    transactions_list, product_list = create_lists(map_gb_tid)

    for tid in transactions_list:
        temp_vett = [0]*len(product_list)
        for p in map_gb_tid[tid]:
            p_index = product_list.index(p)
            temp_vett[p_index] = 1
        
        matrix.append(temp_vett)

    df = pd.DataFrame(data=matrix, columns=product_list)

    return df


def find_itemeset(itemset, product_list):
    prodotti = []

    for i in itemset:
        prodotti.append(product_list[i])

    return str(prodotti)




row_length = 8
transactions = []

with open ('/home/anto/Scrivania/Python_Environment/datasets/online_retail.csv') as f:
    for row in csv.reader(f):
        if len(row) == row_length and row[0][0] not in ['c','C']:
            temp_map = map_for_trans(row)
            transactions.append(temp_map)
        
    transactions.pop(0)
        

map_gb_tid = groupby_tid(transactions)
print("Groupby tid")

df = matrix_trans(map_gb_tid)
print("Matrix created")


print("FP growth :")
fi = fpgrowth(df, 0.01)
print(len(fi))
print(fi.to_string())
print("\n\n")

print("Association rules:")
rules = association_rules(fi, metric='confidence', min_threshold=0.85)
print(rules.to_string())

transactions_list, product_list = create_lists(map_gb_tid)

print("\n\n")

print("\t\t\tASSOCIATIONS:")
print('')

for antecedent,consequent in zip(rules['antecedents'], rules['consequents']):
    print(find_itemeset (list(antecedent), product_list ) +  '  ==>  ' + find_itemeset(list(consequent), product_list))


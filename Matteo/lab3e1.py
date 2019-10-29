import csv
import os
import numpy as np
import pandas as pd
import mlxtend.frequent_patterns as mlx
import timeit 
folderPath = os.getcwd()
slash='/'

def dictLine(cols):
    line={}
    line['InvoiceNo']=cols[0]
    line['StockCode']=cols[1]
    line['Description']=cols[2]
    line['Quantity']=int(cols[3])
    line['InvoiceDate']=cols[4]
    line['UnitPrice']=float(cols[5])
    line['CustomerID']=cols[6]
    line['Country']=cols[7]
    return line

def getInvoiceItems(online_retail):
    invoiceItems={}
    for line in online_retail:
        InvoiceNo=line['InvoiceNo']
        if InvoiceNo[0] not in {'C','c'}:
            if not invoiceItems.keys().__contains__(InvoiceNo):
                invoiceItems[InvoiceNo]=[line['Description']]
            else:
                invoiceItems[InvoiceNo].append(line['Description'])
    
    return invoiceItems

def getItemsSet(invoiceItems):
    s=set()
    for transactionItems in invoiceItems.values():
        s = s | set(transactionItems)
    return list(s)

def getBinaryMatrix(itemsSet,invoiceItems):
    columnMapping={}
    for index,value in enumerate(itemsSet):
        columnMapping[value]=index

    ItemSize=len(itemsSet)
    InvoiceSize=len(invoiceItems)
    binaryMatrix=np.zeros((InvoiceSize,ItemSize))

    row=0
    for transactionItems in invoiceItems.values():
        for item in set(transactionItems):
            binaryMatrix[row][columnMapping[item]]+=1
        row+=1

    return binaryMatrix

def getAntecedents(antecedentsIndices,itemsSet):
    antecedents=[]   
    for k,el in antecedentsIndices.items():
        s=set()
        for index in list(el):
            s.add(itemsSet[index])
        antecedents.append(s)
    
    return antecedents

def getConsequents(consequentsIndices,itemsSet):
    consequents=[]
    for k,el in consequentsIndices.items():
        s=set()
        for index in list(el):
            s.add(itemsSet[index])
        consequents.append(s)
    
    return consequents

"""

• InvoiceNo: Invoice number. Nominal, a 6-digit integral number uniquely assigned to each transaction. 
If this code starts with letter §c’, it indicates a cancellation. 
• StockCode: Product (item) code. Nominal, a 5-digit integral number uniquely assigned to each distinct product.
• Description: Product (item) name. Nominal. 
• Quantity: The quantities of each product (item) per transaction. Numeric. 
• InvoiceDate: InviceDateandtime. Numeric,thedayandtimewheneachtransactionwasgenerated. 
• UnitPrice: Unit price. Numeric, Product price per unit in sterling. 
• CustomerID: Customer number. Nominal, a 5-digit integral number uniquely assigned to each customer. 
• Country: Country name. Nominal, the name of the country where each customer resides. 
"""

#1.
online_retail=[]
with open(folderPath + slash + 'online_retail.csv') as f:
    next(csv.reader(f))
    for i,cols in enumerate(csv.reader(f)):
        line=dictLine(cols)
        online_retail.append(line)

if (len(online_retail) == i+1):
    print('1.\nFile succesfully red\n')
#2.
invoiceItems=getInvoiceItems(online_retail)
print('2.\nItems succesfully associated to each invoiceNo\n')

#3.
itemsSet=getItemsSet(invoiceItems)
binaryMatrix=getBinaryMatrix(itemsSet,invoiceItems)
print('3.\nBinaryMatrix created\n')
df = pd.DataFrame(data=binaryMatrix,columns=itemsSet)
#print(f'DF IS:\n{df}')

#4.
fi = mlx.fpgrowth(df, 0.01)
#print(len(fi)) 
#print(fi.to_string())

#7.
associationRules=mlx.association_rules(fi,metric='confidence',min_threshold=0.85)
print(f'7.\nAssociation rules: {len(associationRules)} elements')
antecedents=getAntecedents(associationRules['antecedents'],itemsSet)
consequents=getConsequents(associationRules['consequents'],itemsSet)

for ant,cons in zip(antecedents,consequents):
    print(f'{ant} ==> {cons}')
#8
"""
print('8.')
support=0.05
print(f'Time to compute fpgrowth having a support of:{support} -> {timeit.timeit(lambda: mlx.fpgrowth(df,support),number=1):.3f} seconds')
print(f'Time to compute apriori having a support of:{support} -> {timeit.timeit(lambda: mlx.apriori(df,support),number=1):.3f} seconds\n')

support=0.02
print(f'Time to compute fpgrowth having a support of:{support} -> {timeit.timeit(lambda: mlx.fpgrowth(df,support),number=1):.3f} seconds')
print(f'Time to compute apriori having a support of:{support} -> {timeit.timeit(lambda: mlx.apriori(df,support),number=1):.3f} seconds\n')

support=0.01
print(f'Time to compute fpgrowth having a support of:{support} -> {timeit.timeit(lambda: mlx.fpgrowth(df,support),number=1):.3f} seconds')
print(f'Not able to compute apriori having a support of:{support}')
"""
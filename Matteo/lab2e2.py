import os
import string
import math
from statistics import mean
folderPath = os.getcwd()
slash='/'


def tokenize(docs):  
    tokens = []
    for doc in docs: 
        for punct in string.punctuation: 
            doc = doc.replace(punct, " ").replace('\n','')
        split_doc = [ token.lower() for token in doc.split(" ") if token ]
        tokens.append(split_doc)
        
    return tokens

def TF(tokens):
    listTF=[]
    for el in tokens:
        tf={}
        for word in el:
            if word not in tf:
                tf[word]=1
            else:
                tf[word]+=1
        if word=='1':
            tf['1']-=1
        if word == '0':
            tf['0']-=1
        listTF.append(tf)
        
    return listTF

def DF(tokens):
    dictDF={}
    for el in tokens:
        for word in set(el):
            if word not in dictDF:
                dictDF[word]=1
            else:
                dictDF[word]+=1
    return dictDF

def IDF(dictDF,N):
    return {k:math.log(N/v) for k,v in dictDF.items()}

def TFIDF(listTF,dictIDF):
    TFIDF=[]
    for el in listTF:
        DocTFIDF={}
        for k,v in el.items():
            DocTFIDF[k]=v*dictIDF[k]
        TFIDF.append(DocTFIDF)
    return TFIDF

def FrattinTFIDF(listTFIDF):
    posTFIDF={}
    sizePos=len(positiveDocuments)
    for el in positiveDocuments:
        for k,v in listTFIDF[el].items():
            if posTFIDF.keys().__contains__(k):
                posTFIDF[k]+=v/sizePos
            else:
                posTFIDF[k]=v/sizePos

    negTFIDF={}
    sizeNeg=len(negativeDocuments)
    for el in negativeDocuments:
        for k,v in listTFIDF[el].items():
            if negTFIDF.keys().__contains__(k):
                negTFIDF[k]+=v/sizeNeg
            else:
                negTFIDF[k]=v/sizeNeg

    return posTFIDF,negTFIDF

    
def norm(d): 
    """Compute the L2-norm of a vector representation.""" 
    return sum([ tf_idf**2 for t, tf_idf in d.items() ])**.5

def dot_product(d1, d2):
    """Compute the dot product between two vector representations."""
    word_set = set(d1.keys())&set(d2.keys())
    return sum([( d1.get(d, 0.0) * d2.get(d, 0.0)) for d in word_set ])
def cosine_similarity(d1, d2):
    """ Compute the cosine similarity between documents d1 and d2.
    Input: two dictionaries representing the TF-IDF vectors for documents d1 and d2. Output: the cosine similarity. """
    return dot_product(d1, d2) / (norm(d1) * norm(d2))

def computeAll_cosine_similarity(positiveDocuments,negativeDocuments,testDocument,listTFIDF):
    similarityPos=[]
    similarityNeg=[]
    for indexPos in positiveDocuments:
        similarityPos.append(cosine_similarity(testDocument,listTFIDF[indexPos]))
    for indexNeg in negativeDocuments:
        similarityNeg.append(cosine_similarity(testDocument,listTFIDF[indexNeg]))
    
    return similarityPos,similarityNeg

#2.
with open(folderPath + slash + 'documents.txt',encoding='utf-8') as dataset:
    documents = [line for line in dataset]

del documents[0] #Delete header line 
tokens=tokenize(documents)

#3.
listTF=TF(tokens)
print(f'3. Testing TF results:\nToken "the" occurs {listTF[0]["the"]} times in the first document\n')

#4.
dictDF=DF(tokens)
print(f'4. Testing DF reults:\nToken "the" occurs in {dictDF["the"]} documents\n')

dictIDF = IDF(dictDF,len(documents))
sortListIDF=sorted(dictIDF.items(),key=lambda kv:kv[1])
print(f'4. Testing IDF result:\n 10 Tokens having lowest IDF:\n{sortListIDF[0:11]}\n')

#5.
listTFIDF=TFIDF(listTF,dictIDF)
#print(f'TFIDF[0] is {listTFIDF[0]}')

#6.

#a)
testPositiveDocument=listTFIDF[0]

#b)
positiveDocuments=[i for i,el in enumerate(tokens) if el[-1]=='1'] #Contains indices concerning positive document among all documents
negativeDocuments=[i for i,el in enumerate(tokens) if el[-1]=='0']

#c)
similarityPos,similarityNeg=computeAll_cosine_similarity(positiveDocuments,negativeDocuments,testPositiveDocument,listTFIDF)

#d)
rate='Positive' if positiveDocuments.__contains__(0) else 'Negative'

#e) 
meanPos=mean(similarityPos)
meanNeg=mean(similarityNeg)
myrate='Positive' if meanPos>=meanNeg else 'Negative'

print('6. e)Sentiment analysys by computing test document:\n["PositiveMean","NegativeMean","RealRate","MyRate"]')
print(f'[{meanPos:.6f},{meanNeg:.6f},{rate},{myrate}]\n')

#f)
#Fabio Frattin

posTFIDF,negTFIDF=FrattinTFIDF(listTFIDF)
print('6. e)Sentiment analysys by computing test document (Frattin method):\n["PositiveMean","NegativeMean","RealRate","MyRate"]')
meanPos=cosine_similarity(testPositiveDocument,posTFIDF)
meanNeg=cosine_similarity(testPositiveDocument,negTFIDF)
myrate='Positive' if meanPos>=meanNeg else 'Negative'
print(f'[{meanPos:.4f},{meanNeg:.4f},{rate},{myrate}]')

#print(len(posTFIDF))
#print(sorted(posTFIDF.items(),key = lambda kv:kv[1],reverse=True)[0:100])

meanSimilarity=[["PositiveMean","NegativeMean","RealRate","MyRate"]]
correctAnalysis=[]
totalDocuments=len(listTFIDF)
print('Percentage of correct sentiment analisys is:')
for index,el in enumerate(listTFIDF):
    posResult=cosine_similarity(el,posTFIDF)
    negResult=cosine_similarity(el,negTFIDF)
    rate = 'Positive' if positiveDocuments.__contains__(index) else 'Negative'
    myrate='Positive' if posResult>=negResult else 'Negative'
    correctAnalysis.append(1) if rate==myrate else correctAnalysis.append(0)
    print (f'{mean(correctAnalysis)*100:.2f}% ({index+1}/{totalDocuments} documents analysed)',end='\r')

print('\n')
correctAnalysis.clear()
for index,el in enumerate(listTFIDF):   
    #Return all cosine similarity between el-document and all positive and negative docuements, separately.
    similarityPos,similarityNeg=computeAll_cosine_similarity(positiveDocuments,negativeDocuments,el,listTFIDF)

    #Check correctness of the 2 lists above
    #print(f'Intersection between negative and positive documents contains: {len(set(similarityNeg)&set(similarityPos))} elements') 

    rate = 'Positive' if positiveDocuments.__contains__(index) else 'Negative'
    meanPos=mean(similarityPos)
    meanNeg=mean(similarityNeg)
    myrate='Positive' if meanPos>=meanNeg else 'Negative'
    meanSimilarity.append([meanPos,meanNeg,rate,myrate])

    correctAnalysis.append(1) if rate==myrate else correctAnalysis.append(0)
    print (f'{mean(correctAnalysis)*100:.2f}% ({index+1}/{totalDocuments} documents analysed)',end='\r')















import string

def tokenize(docs):
# """Compute the tokens for each document.
# Input: a list of strings. Each item is a document to tokenize.
# Output: a list of lists. Each item is a list containing the tokens of the
# relative document.
# """
    tokens = []
    for doc in docs:
        for punct in string.punctuation:
            doc = doc.replace(punct, " ")
            split_doc = [ token.lower() for token in doc.split(" ") if token ]
            tokens.append(split_doc)

    return tokens

dataset = []

with open ('/home/anto/Scrivania/Python_Environment/datasets/aclimdb_reviews_train.txt','r') as f:
    for row in f.readlines():
        print(row)
        dataset.append(row)
        print("row computed")

print('Beginning to tokenize')
dataset = tokenize(dataset)
print('DONE')
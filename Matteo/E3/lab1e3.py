import csv
import os
import Classes.mnist as m
folderPath = os.getcwd()
slash='/'

mnist = m.Mnist()
with open(folderPath + slash + 'mnist.csv') as f: 
    for cols in csv.reader(f):
        mnist.insertDigit(cols)

#2. Create a function that, given a position 1 ≤ k ≤ 10,000, prints the kth digit of the dataset (i.e. the kth row of the csv ﬁle) as a grid of 28×28 characters. More speciﬁcally, you should map each range of pixel values to the following characters: • [0,64) →" " • [64,128) →"." • [128,192) →"*" • [192,256) →"#" So, for example, you should map the sequence 0, 72, 192, 138, 250 to the string " .#*#". For Figure 2 (which is the 130th image in the dataset), the resulting output would be:
print('2.')
mnist.printDigit(130)

#3. Compute the Euclidean distance between each pair of the 784-dimensional vectors of the digits at the following positions: 26th, 30th, 32nd, 35th
print('3.')
list1=[26,30,32,35]
euclideanDistancesDict = mnist.euclideanDistances(list1) # euclideanDistanceDict is a dictionary having pair elements as key (separated by ';') and euclidean distance as value
for k,v in euclideanDistancesDict.items():
    print(f'\tThe pair {k} is at a distance of {v}')

# 5. (*) There are 1,135 1’s and 980 0’s in the dataset. For all 0’s and 1’s separately, count the number oftimeseachofthe784pixelsisblack(use128asthethresholdvalue). Youcandothisbybuilding alist Z andalist O,eachcontaining784elements, containingrespectivelythecountsforthe0’sand the 1’s. Z[i] and O[i] contain the number of times the ith pixel was black for either class. For each value i, compute abs(Z[i] - O[i]). The i with the highest value represents the pixel that best separatesthedigits“0”and“1”(i.e. thepixelthatismostoftenblackforoneclassandwhiteforthe other). Where is this pixel located within the grid? Why is it?
print('5.')
contrast,index=mnist.highestContrast(128)
print(f'\tThe highest contrast is: {contrast}. In the grid, it is the {index}th pixel.')




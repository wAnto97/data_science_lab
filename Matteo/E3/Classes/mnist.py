import math
import functools

class Mnist:

    pixel_size=28
    digitsLen=0

    def __init__(self):
        self.listOfDigits=[]
        self.digits={}
        self.decodeDigits={'0;63':' ','64;127':'.','128;191':'*','192;255':'#'}
        self.blackOccurences={}
       

    def insertDigit(self,values):
        matrix=[]
        listToAdd=[]
        self.listOfDigits.append(int(values[0]))

        for i in range(0,self.pixel_size):
            for j in range(0,self.pixel_size):
                listToAdd.append(int(values[self.pixel_size*i + j +1]))
            matrix.append(listToAdd)
            listToAdd=[]

        self.digits[self.digitsLen]=matrix
        self.digitsLen+=1

    

    def printDigit(self,row):
        stringDecoded=''
        digit=self.digits[row-1]

        for l1 in digit:
            for l2 in l1:
                stringDecoded += self.decode(l2)
            print(stringDecoded+'\n')
            stringDecoded=''
        
        
    def decode(self,resolution):
        
        """
        for k,v in self.decodeDigits.items():
            interval=k.split(';')
            if resolution >= int(interval[0]) and resolution <= int(interval[1]):
                return v
            """
        #Alternative solution using filter and map methods.
        keys=list(self.decodeDigits.keys())
        values=list(self.decodeDigits.values())
        return list(filter(lambda x : resolution >= int(x[0]) and resolution <= int(x[1]),map(lambda  k,v: [k.split(';')[0],k.split(';')[1],v],keys,values)))[0][2]

    def computeEuclideanDistances(self,matrix1,matrix2):
        somma=0
        for i in range(0,self.pixel_size):
            for j in range(0,self.pixel_size):
                somma+=(matrix1[i][j] - matrix2[i][j])**2
        
        return math.sqrt(somma)
    
    def euclideanDistances(self,list1):
        euclideanDistancesMap = {}
        for i in range(0,len(list1)):
            for j in range(i+1,len(list1)):
                distance=self.computeEuclideanDistances(self.digits[list1[i]-1],self.digits[list1[j]-1])
                key=str(list1[i]) + ';' + str(list1[j])
                euclideanDistancesMap[key]=distance
        
        return euclideanDistancesMap

    def zeroListMaker(self,n):
         listOfZeros = [0] * n
         return listOfZeros

    def highestContrast(self,threshold):
        ones=self.zeroListMaker(self.pixel_size*self.pixel_size)
        zeros=self.zeroListMaker(self.pixel_size*self.pixel_size)
        flatten = lambda l: [item for sublist in l for item in sublist]
        
        for d,v in zip(self.listOfDigits,self.digits.values()):
            if d==0:
                v=flatten(v)
                for i,el in enumerate(v):
                    if el > threshold:
                        zeros[i]+=1

            if d==1:
                v=flatten(v)
                for i,el in enumerate(v):
                    if el > threshold:
                        ones[i]+=1
    
        absDiff = [math.fabs(x-y) for x,y in zip(ones,zeros)]
        x=max([value,index] for index,value in enumerate(absDiff))

        #Alternative solution to calculate maxAbsDiff
        """
        index = -1
        maxDistance=-1

        for i in range(0,self.pixel_size*self.pixel_size):
            absDiff = math.fabs(ones[i] - zeros[i])
            if absDiff > maxDistance:
                maxDistance = absDiff
                index = i"""

        return x


    
    
    

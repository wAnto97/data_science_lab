import csv
import os
import matplotlib.pyplot as plt
folderPath = os.getcwd()
slash='/'

def replaceBeginning(leftShift,v,i):
    if leftShift==1:
            v[0]=v[i]/2
    if leftShift>1:
        for rightShift in range(0,leftShift):
            if rightShift==0:
                v[0]=v[i]/2
            else:
                v[i-leftShift+rightShift]=(v[i-leftShift+rightShift-1]+v[i])/2

def replaceEnd(leftShift,v,i,list_size):
    if leftShift==1:
        v[list_size-1]=v[i-leftShift-1]/2
    if leftShift>1:
        for rightShift in range(0,leftShift):
            if rightShift==0:
                v[list_size-1]=v[list_size-1-leftShift]/2
            else:
                v[list_size-1-rightShift]=(v[list_size -1 - rightShift +1] +v[list_size-1-leftShift])/2

def replace(leftShift,v,i):
    for rightShift in range(0,leftShift):
        v[i-leftShift+rightShift]=(v[i-leftShift+rightShift-1]+v[i])/2

def measurements(city,N,temperatureCityDict):
    hottestTemperature=[]
    coldestTemperature=[]
    temperatureLists=temperatureCityDict[city]
    if temperatureLists != None:
        for index,el in enumerate(temperatureLists):
            if index<=N:
                if index==N:
                    minHotValue,indexMinHotValue=min((v,i) for i,v in enumerate(hottestTemperature))
                    maxColdValue,indexMaxColdValue=max((v,i) for i,v in enumerate(coldestTemperature))
                else:
                    hottestTemperature.append(el)
                    coldestTemperature.append(el)
            else:
                if el > minHotValue:
                    del hottestTemperature[indexMinHotValue]
                    hottestTemperature.append(el)
                    minHotValue,indexMinHotValue=min((v,i) for i,v in enumerate(hottestTemperature))

                if el < maxColdValue:
                    del coldestTemperature[indexMaxColdValue]
                    coldestTemperature.append(el)
                    maxColdValue,indexMaxColdValue=max((v,i) for i,v in enumerate(coldestTemperature))
    
    return hottestTemperature,coldestTemperature



    
#1.
globalLandTemperature=[]
with open(folderPath + slash + 'GlobalLandTemperature.csv') as f:
    next(csv.reader(f))
    for cols in csv.reader(f):
        globalLandTemperature.append(list(cols))

temperatureCityDict={}
for row in globalLandTemperature:
    if not temperatureCityDict.keys().__contains__(row[3]):
        if row[1]!='':
            temperatureCityDict[row[3]]=[float(row[1])]
        else:
            temperatureCityDict[row[3]]=[None]
    else:
        if row[1]!='':
            temperatureCityDict[row[3]].append(float(row[1]))
        else:
            temperatureCityDict[row[3]].append(None)


#2.
for k,v in temperatureCityDict.items():
    found=False
    isFirst=False
    isLast=False
    rightShift,leftShift=0,0
    list_size=len(v)
    for i in range(0,list_size):

        if v[i]==None:
            if i==0:
                isFirst=True
            if i==list_size-1:
                isLast=True
            leftShift+=1
            found=True
            continue

        if found:
            if isFirst:
                replaceBeginning(leftShift,v,i)
            else:
                replace(leftShift,v,i)

        found=False
        isFirst=False
        leftShift=0

    if isLast:
        replaceEnd(leftShift,v,i,list_size)
                
#3.  
N=4                  
city='Rome'    
hottestTemperatures,coldestTemperatures=measurements(city,N,temperatureCityDict)
print('3.')
print(f'The {N} hottest temperatures in {city} are:\n{hottestTemperatures}')
print(f'The {N} coldest temperatures in {city} are:\n{coldestTemperatures}')

#4.
plt.figure('Rome [°C]')
plt.hist(temperatureCityDict['Rome'])


plt.figure('Bangkok [°F]')
plt.hist(temperatureCityDict['Bangkok'])

#5.
temperatureCityDict['Bangkok']=[(el-32)/1.8 for el in temperatureCityDict['Bangkok']]

plt.figure('Bangkok [°C]')
plt.hist(temperatureCityDict['Bangkok'])

plt.show()



            
        





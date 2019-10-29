import csv
import matplotlib.pyplot as plt
from random import gauss

def mapify(row):
    output = {}
    keys = ['Date','AverageTemperature','AverageTemperatureUncertainty','City','Country','Latitude','Longitude']

    for i in range(0,len(keys)):
        output[keys[i]] = row[i]
    
    return output


def clean_dataset(dataset):
    for [index,row] in enumerate(dataset):
        if(row['AverageTemperature'] == ''): #Temperature missing

            if (index == 0 or dataset[index-1]['City'] != row['City']): #First value
                prevTemp = 0
                nextTemp = searchNext(dataset, row['City'], index)

            elif(index == len(dataset)-1 or dataset[index+1]['City'] != row['City']): #Last value
                prevTemp = float(dataset[index-1]['AverageTemperature'])
                nextTemp = 0

            else:
                prevTemp = float(dataset[index-1]['AverageTemperature'])
                nextTemp = searchNext(dataset, row['City'], index)

            row['AverageTemperature'] = str((prevTemp + nextTemp)/2)    
        


def ranks (dataset, city, N):
    cityTemp = list(filter(lambda x : x['City'] == city, dataset))
    list.sort(cityTemp, key = lambda x : float(x['AverageTemperature']), reverse=True)
    hottest = cityTemp[:N]
    coldest = cityTemp[-N:]
    print('Coldest ' + str(N))
    print(coldest)
    print('Hottest ' + str(N))
    print(hottest)

def searchNext(dataset, city, start):
    index = start + 1
    while (dataset[index]['City'] == city):
        if(dataset[index]['AverageTemperature'] != ''):
            return float(dataset[index]['AverageTemperature'])

        index += 1
    
    return 0


def change_scale(dataset, city):
    for row in dataset:
        if(row['City'] == city):
            row['AverageTemperature'] = (float(row['AverageTemperature']) - 32)/1.8
    


def plot_list (dataset, city):
    cityTemp = list(filter(lambda x : x['City'] == city, dataset))
    return list(map(lambda x : float(x['AverageTemperature']), cityTemp))


dataset = []

with open ('/home/anto/Scrivania/Python_Environment/GLT_filtered.csv') as f:
    for row in csv.reader(f):
        dataset.append(mapify(row))
    dataset.pop(0) #Remove the first line (Attributes)

clean_dataset(dataset) #Inserting missing avgTemp values

change_scale(dataset, 'Bangkok') # Fahreneit to Celsius

ranks(dataset,'Bangkok',3)

plotted = plot_list(dataset, 'Bangkok')
plt.hist(plotted)
plt.title('Bangkok')
plotted = plot_list(dataset, 'Rome')
plt.figure(2)
plt.hist(plotted)
plt.title('Rome')
plt.show()




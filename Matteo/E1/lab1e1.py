import csv
from Classes.iris import Iris
import os
folderPath = os.getcwd()
slash='/'

iris = Iris()
with open(folderPath + slash + 'iris.csv') as f: 
    for cols in csv.reader(f): 
        if len(cols) == 5:
            iris.insertFloat(float(cols[0]),float(cols[1]),float(cols[2]),float(cols[3]))

a,b,c,d = iris.calculate_mean()
print(f'media sepal width:{a}\nmedia sepal length:{b}\nmedia petal width:{c}\nmedia petal length:{d}')

#Mi scocciavo di fare gli altri punti
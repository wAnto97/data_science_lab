class Iris:

    def __init__(self):
        self.sepal_width=[]
        self.sepal_length=[]
        self.petal_width=[]
        self.petal_length=[]

    def insertFloat(self,a,b,c,d):
        self.sepal_width.append(a)
        self.sepal_length.append(b)
        self.petal_width.append(c)
        self.petal_length.append(d)
        return

    def calculate_mean(self):
        mean_sepal_width=0.0    
        mean_sepal_length=0.0
        mean_petal_width=0.0
        mean_petal_length=0.0

        for el in self.sepal_width:
            mean_sepal_width+=el
    
        for el in self.sepal_length:
            mean_sepal_length+=el
    
        for el in self.petal_length:
            mean_petal_length+=el
    
        for el in self.petal_width:
            mean_petal_width+=el

        return mean_sepal_width/len(self.sepal_width),mean_sepal_length/len(self.sepal_length),mean_petal_width/len(self.petal_width),mean_petal_length/len(self.petal_length)


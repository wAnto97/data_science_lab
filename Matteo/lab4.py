import numpy as np 
import os 
import matplotlib.pyplot as plt
import KMeans as KMeansClass

folderPath = os.getcwd()
slash = '/'

def ChooseK(KSet,dataset,kmeans):

    numpyKSet=np.array(KSet)
    sizeKSet=numpyKSet.size
    numpySilhouette=2*np.ones(numpyKSet.size)
    for i in range(0,sizeKSet):
        k=numpyKSet[i]
        kmeans.fit_predict(5)
        numpySilhouette[i]=kmeans.silhouette_score()
        print(f'\tK={k}\tSilhouette score:{numpySilhouette[i]}')
    
    ax=plt.subplots(figsize=(8,5))[1]
    ax.plot(numpyKSet,numpySilhouette)
    plt.show()




#1.1
GaussianClusters2D= np.loadtxt(folderPath + slash + '2D_gauss_clusters.txt',delimiter=',')
Chameleon=np.loadtxt(folderPath + slash + 'chameleon_clusters.txt',delimiter=',')

#1.2

def scatterPlot(dataset):
    ax=plt.subplots(figsize=(5,3))[1]
    colors=dataset[:,0] + dataset[:,1]
    ax.scatter(dataset[:,0],dataset[:,1],c=colors)
    plt.show()    

scatterPlot(GaussianClusters2D)
scatterPlot(Chameleon)


#1.5
for k in range(10,30):
    GaussianKmeans=KMeansClass.KMeans(k,len(GaussianClusters2D),GaussianClusters2D,300*1000, 700*1000)
    GaussianKmeans.fit_predict(5)
    print(f'\tSSE:{GaussianKmeans.calculateSSE()} K={k}' )
    #K=15 

for k in range(1,15):
    ChameleonKmeans=KMeansClass.KMeans(k,len(Chameleon),Chameleon,200,500)
    ChameleonKmeans.fit_predict(5) #6,7
    print(f'SSE:{ChameleonKmeans.calculateSSE()} K={k}' )
    #K=6,7


#2.3
KSet=[14,15,16]
print(f'Gaussian Dataset. Choosing K...')
ChooseK(KSet,GaussianClusters2D,GaussianKmeans)

print(f'\n\nChameleon Dataset. Choosing K...')
KSet=[2,3,4,5,6,7,8,9,10,11,20]
ChooseK(KSet,Chameleon,ChameleonKmeans)

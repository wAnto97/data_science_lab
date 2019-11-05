import numpy as np
import matplotlib.pyplot as plt
import os

class KMeans:
  
    class Centroids:
        def __init__(self,K,InitialCentroids):

            self.clusters=np.zeros((K,6)) #Columns: 'x,y,SumX,SumY,NumOfPoints,ClusterID'
            self.x,self.y,self.SumX,self.SumY,self.NumberOfPoints,self.ClusterID=0,1,2,3,4,5

            self.clusters[:,:2]=InitialCentroids[:,:2]
            self.clusters[:,2:4]=InitialCentroids[:,:2]
            self.clusters[:,4]=np.ones((K),dtype='int')
            self.clusters[:,5]=np.arange(K)


        
        def getClosestCluster(self,x,y):

            minDistance=((x-self.clusters[0,self.x])**2 + (y-self.clusters[0,self.y])**2)**.5
            clusterID=0
            for i in range(1,len(self.clusters)):
                distance=((x-self.clusters[i,self.x])**2 + (y-self.clusters[i,self.y])**2)**.5
                if (distance < minDistance):
                    minDistance=distance
                    clusterID=i
            
            self.clusters[clusterID,self.SumX]+=x
            self.clusters[clusterID,self.SumY]+=y
            self.clusters[clusterID,self.NumberOfPoints]+=1
            
            return clusterID
        
        def refreshCentroids(self):
            sizeClusters=len(self.clusters)
            for i in range(0,sizeClusters):
                if self.clusters[i,self.x]!=self.clusters[i,self.SumX]/self.clusters[i,self.NumberOfPoints] or self.clusters[i,self.y]!=self.clusters[i,self.SumY]/self.clusters[i,self.NumberOfPoints]:
                    break
            
            if i==sizeClusters-1:
                return False

            for i in range(0,sizeClusters):
                self.clusters[i,self.x]=self.clusters[i,self.SumX]/self.clusters[i,self.NumberOfPoints]
                self.clusters[i,self.y]=self.clusters[i,self.SumY]/self.clusters[i,self.NumberOfPoints]

                self.clusters[i,self.SumX]=0
                self.clusters[i,self.SumY]=0
                self.clusters[i,self.NumberOfPoints]=0

            return True

        def CheckEmptyClusters(self):

            foundEmptyCluster=False
            counter=0
            indicesEmptyClusters=[]
            for i in range(0,len(self.clusters)):
                if self.clusters[i,self.NumberOfPoints]==0:
                    foundEmptyCluster=True
                    counter+=1
                    indicesEmptyClusters.append(i)
            return foundEmptyCluster,counter,indicesEmptyClusters


    class Labels:
        def __init__(self,N,NumpyPoints):
            self.points=np.zeros((N,5)) #Columns: 'x,y,ClusterID,PointID,SilhouetteScore' ClusterID -> index of corresponding cluster in Centroids
            self.x,self.y,self.ClusterID,self.PointID,self.SilhouetteScore=0,1,2,3,4

            self.points[:,self.x],self.points[:,self.y]=NumpyPoints[:,self.x],NumpyPoints[:,self.y]
            self.points[:,self.ClusterID]=-1*np.ones((N),dtype="int")
            self.points[:,self.PointID]=np.arange((N))
            self.points[:,self.SilhouetteScore]=2*np.ones(N)

    
    
    def __init__(self,n_clusters,n_points,NumpyPoints,lowValue,highValue,max_iter=100):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.labels = self.Labels(n_points,NumpyPoints)
        self.centroids = self.Centroids(n_clusters,np.random.randint(low=lowValue,high=highValue,size=(n_clusters,2)))


    #3.
    def fit_predict(self,step=1,plot_clusters=False):
        """Run the K-means clustering on X.
        :param X: input data points, array, shape = (N,C).
        :return: labels : array, shape = N.
        """

        def computeNewCentroids(self):
            isEmpty,emptyCounter,indicesEmptyClusters=self.centroids.CheckEmptyClusters()
            if isEmpty:
                print(f'Sono vuoti:{indicesEmptyClusters}')
                calculateNewCentroids(self,emptyCounter,indicesEmptyClusters)
            return self.centroids.refreshCentroids()

        def calculateNewCentroids(self,emptyCounter,indicesEmptyClusters):
            
            N=len(self.labels.points)
            listSSE=np.zeros((N,3))
            for i in range(0,N):
                XPoint=self.labels.points[i,self.labels.x]
                YPoint=self.labels.points[i,self.labels.y]

                ClusterID=int(self.labels.points[i,self.labels.ClusterID])
                XCluster=self.centroids.clusters[ClusterID,self.centroids.x]
                YCluster=self.centroids.clusters[ClusterID,self.centroids.y]
                
                listSSE[i,0]=XPoint
                listSSE[i,1]=YPoint
                listSSE[i,2]=(XPoint - XCluster)**2 + (YPoint - YCluster)**2
            
            newCentroids=np.sort(listSSE.view('float,float,float'),order=['f2'],axis=0).view(np.float)[0:emptyCounter,[0,1]]
            print(newCentroids)
            
            for i,indexEmptyCluster in enumerate(indicesEmptyClusters):
                self.centroids.clusters[indexEmptyCluster,[0,1]]=newCentroids[i,:]
                self.centroids.clusters[indexEmptyCluster,[2,3]]=newCentroids[i,:]
                self.centroids.clusters[indexEmptyCluster,4]+=1
        
        def printCentroidsCoordinates(self):

            print('Centroids Coordinates')
            print(f'{self.centroids.clusters[:,[self.labels.x,self.labels.y]]}')


        #Main Function
        NumberOfPoints=len(self.labels.points)
        for iter in range(0,self.max_iter):
            for i in range(0,NumberOfPoints):
                self.labels.points[i,self.labels.ClusterID]= self.centroids.getClosestCluster(self.labels.points[i,self.labels.x],self.labels.points[i,self.labels.y])
            
            if not computeNewCentroids(self):
                print(f'Break executed. iter={iter+1}')
                break

            if plot_clusters:
                self.stepShow(iter+1,step)           
        self.show()
        
        return self.labels.points[:,[self.labels.PointID,self.labels.ClusterID]]


    #1.4
    def dump_to_file(self, filename):
        """Dump the evaluated labels to a CSV file."""
        file=open(os.getcwd()+'/' + filename,"w+")
        file.write("Id,ClusterId\n")
        for i in range(0,len(self.labels.points)):
            file.write(f'{i},{int(self.labels.points[i,self.labels.ClusterID])}\n')
        
        file.close()

    #1.6.
    def show(self):
        ax=plt.subplots(figsize=(8,5))[1]
        pointsX,pointsY=self.labels.points[:,self.labels.x],self.labels.points[:,self.labels.y]
        centroidX,centroidY=self.centroids.clusters[:,self.centroids.x],self.centroids.clusters[:,self.centroids.y]
        
        ax.scatter(pointsX,pointsY,c=self.labels.points[:,self.labels.ClusterID])
        ax.plot(centroidX,centroidY,c='red',linestyle='',marker='*')
        plt.show()
    

    #1.7
    def stepShow(self,iteration,step):
        if iteration % step ==0:
            self.show()


    #2.1
    def silhouette_samples(self):
        """Evaluate the silhouette for each point and return them as a list.
        :param X: input data points, array, shape = (N,C).
        :param labels: the list of cluster labels, shape = N.
        :return: silhouette : array, shape = N
        """

        
        def calculateAverageSimilarity(self,x,y,PointsInCluster):

            averageSimilarity=np.zeros((len(PointsInCluster)))
            for i in range(0,len(PointsInCluster)):
                XPointCluster=PointsInCluster[i,self.labels.x]
                YPointClutser=PointsInCluster[i,self.labels.y]

                averageSimilarity[i]=((x-XPointCluster)**2 + (y-YPointClutser)**2)**.5
        
            return averageSimilarity.mean()

        def getListOfPointsNotInCluster(self,PointsInCluster,ClusterID):

            list1=[]
            for i,el in enumerate(PointsInCluster):
                if (i!=ClusterID):
                    list1.append(el)
            return list1
        
        
        def calculateLowestAverageDissimilarity(self,x,y,ListPointsNotInCluster):

            minDissimilarity=-1
            for PointsNotInCluster in ListPointsNotInCluster:
                averageDissimilarity=np.zeros((len(PointsNotInCluster)))
                for i in range(0,len(PointsNotInCluster)):
                    XPointCluster=PointsNotInCluster[i,self.labels.x]
                    YPointClutser=PointsNotInCluster[i,self.labels.y]

                    averageDissimilarity[i]=((x-XPointCluster)**2 + (y-YPointClutser)**2)**.5
                
                meanDissimilarity=averageDissimilarity.mean()
                if(minDissimilarity==-1):
                    minDissimilarity=meanDissimilarity
                else:
                    if(meanDissimilarity<minDissimilarity):
                        minDissimilarity=meanDissimilarity
            
            return minDissimilarity
        
        def calculateSilhouetteScore(self,a,b):
            return (b-a)/max([a,b])



        #Main Function
        ClusterIDs=set(self.labels.points[:,self.labels.ClusterID])
        PointsInCluster=[]
        for el in ClusterIDs:
            mask=self.labels.points[:,self.labels.ClusterID]==el
            PointsInCluster.insert(int(el),self.labels.points[mask])
       
        for i in range(0,len(self.labels.points)):
            ClusterID=int(self.labels.points[i,self.labels.ClusterID])
            averageSimilarity=calculateAverageSimilarity(self,self.labels.points[i,self.labels.x],self.labels.points[i,self.labels.y],PointsInCluster[ClusterID])
            PointsNotInCluster=getListOfPointsNotInCluster(self,PointsInCluster,ClusterID)
            lowestAverageDissimilarity=calculateLowestAverageDissimilarity(self,self.labels.points[i,self.labels.x],self.labels.points[i,self.labels.y],PointsNotInCluster)

            self.labels.points[i,self.labels.SilhouetteScore]=calculateSilhouetteScore(self,averageSimilarity,lowestAverageDissimilarity)
        
        return self.labels.points[:,self.labels.SilhouetteScore]


    #2.1
    def silhouette_score(self):
        """Evaluate the silhouette for each point and return the mean.
        :param X: input data points, array, shape = (N,C).
        :param labels: the list of cluster labels, shape = N.
        :return: silhouette : float
        """
        self.silhouette_samples()
        return self.labels.points[:,self.labels.SilhouetteScore].mean()



    def calculateSSE(self):
        SSE=0
        for i in range(0,len(self.labels.points)):
            XPoint=self.labels.points[i,self.labels.x]
            YPoint=self.labels.points[i,self.labels.y]

            ClusterID=int(self.labels.points[i,self.labels.ClusterID])
            XCluster=self.centroids.clusters[ClusterID,self.centroids.x]
            YCluster=self.centroids.clusters[ClusterID,self.centroids.y]
            
            SSE+=(XPoint - XCluster)**2 + (YPoint - YCluster)**2
    
        return SSE
    
 
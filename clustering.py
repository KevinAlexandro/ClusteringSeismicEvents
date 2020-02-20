import pandas as pd
import matplotlib.pylab as plt
from sklearn.cluster import AgglomerativeClustering as cure
import scipy.cluster.hierarchy as sch
from sklearn.cluster import KMeans
import bfr
from sklearn.manifold import TSNE
from sklearn.metrics import accuracy_score


lisstd=[]
listDis=[]
distK=[]
distS=[]
acc={}
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'grey', 'orange', 'purple']
markers = ['o','^','s','.', ',', 'x', '+', 'v', 'd','>']



def tsneG(X):
    tsne = TSNE(n_components=2, random_state=0)
    X_2d = tsne.fit_transform(X)
    dat= pd.DataFrame()
    dat['x1'] = X_2d[:,0]
    dat['y1']= X_2d[:,1]

    plt.scatter(dat["x1"],dat["y1"])
    plt.title("Raw data with no clusters")
    plt.grid()
    fig = plt.gcf()
    fig.canvas.set_window_title('Project 7')
    plt.savefig("raw.png")
    plt.close()

def Cure(input_data,n):
    cure_instance = cure(n_clusters=n, linkage="average", affinity="euclidean")  #also test with affinity ="cosine"
    cure_instance.fit(input_data)
    pred = cure_instance.labels_
    print(pred)
    print("ACC: " + str(accuracy_score(pred, labels)))
    acc["CURE" + str(n)]= str(accuracy_score(pred, labels))
    tsnePlot(pred, n, input_data, 'CURE')

#kmeans implemenation
def kmeans(X,n):
    kmeans = KMeans(n_clusters=n, init='k-means++',precompute_distances='auto').fit(X)
    distK.append(kmeans.inertia_)
    pred= kmeans.predict(X)
    print(kmeans.cluster_centers_)
    print(pred)
    print("ACC: \n" + str(accuracy_score(pred, labels)))
    acc['KMeans'+str(n)] = accuracy_score(pred, labels)
    tsnePlot(pred,n, X,'KMEAN')

#Generate dendoram plot
def dendogram(Mat):
    dendogram = sch.dendrogram(sch.linkage(Mat, method='ward'))
    plt.title("Generated Tree with CURE clustering")
    plt.savefig("CureDend.png")
    plt.show()
    plt.close()


def BFR(Mat,n):
    model = bfr.Model(mahalanobis_factor=3.0, euclidean_threshold=3.0,
                      merge_threshold=2.0, dimensions=83,
                      init_rounds=40, nof_clusters=n)

    Mat = Mat.to_numpy()
    print(Mat.shape)

    model.fit(Mat)

    model.finalize()
    std= model.error()
    dis= model.error(Mat)#/598
    print(dis)
    lisstd.append(std)
    listDis.append(dis)
    print("Desviacion estandar del modelo:\n"+str(model.error()))
    print("SSE del modelo:\n" + str(model.error(Mat)))

    centers = pd.DataFrame(model.centers())
    print(centers)
    pred= model.predict(Mat)



    print("ACC: "+str(accuracy_score(pred,labels)))
    acc['BFR' +str(n)]=accuracy_score(pred,labels)
    print(pred)

    print(pred.shape)
    print(model)
    tsnePlot(pred,n,Mat,'BFR')



def tsnePlot(pred, n,Mat,alg):
    tsne = TSNE(n_components=2, random_state=0)
    X_2d = tsne.fit_transform(Mat)
    dat = pd.DataFrame()
    dat['x1'] = X_2d[:, 0]
    dat['y1'] = X_2d[:, 1]

    klus = list(range(n))

    for i, c,m in zip(klus, colors,markers):
        plt.scatter(X_2d[pred == i, 0], X_2d[pred == i, 1],marker=m, c=c, label=i)

    plt.savefig("Clusters"+alg+str(n)+".png")
    #plt.show()
    plt.close()

def graphCurves():
    plt.figure(figsize=(10,10))
    plt.subplot(2,1,1)
    plt.plot(range(1,10),lisstd,'o-',label="STD")
    plt.title("Desviacion estandar por # clusters")
    plt.grid()
    plt.ylabel("STD")

    plt.subplot(2,1,2)
    plt.plot(range(1,10),listDis,label="Dist",color='red')
    plt.grid()
    plt.title("Average distance vs  #clusters")
    plt.ylabel("Avg. Distance")
    plt.xlabel("# Clusters")
    plt.savefig("FinalCurves.png")
    plt.close()

def graphK(dist):
    plt.plot(range(1,10),dist)
    plt.grid()
    plt.title("Average distance vs  #clusters")
    plt.ylabel("Avg. Distance")
    plt.xlabel("# Clusters")
    plt.savefig("FinalCurvesK.png")
    plt.close()

if __name__ == '__main__':

    matrix = pd.read_csv("features_Modified.csv", delimiter=',', header= None)
    labels = pd.read_csv('labels(1VT-0LP).csv',header=None)

    #Starting BFR tests
    print("BFR TEST:\n")
    for i in range(2,11):
        BFR(matrix, i)    
    #Start kmenas Test
    print("K MEANS  TEST:\n")
    for i in range(2, 11):
        kmeans(matrix, i)

    #Start Cure test
    print("CURE  TEST:\n")
    for i in range(2, 11):
        Cure(matrix, i)
    #subprocess.call("python3 Cure.py ", shell=True)

    print(acc)


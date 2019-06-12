# Tudor Berariu, 2016

from sys import argv
from zipfile import ZipFile
from random import randint

import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt
import matplotlib.markers
from mpl_toolkits.mplot3d import Axes3D

def dummy(Xs):
    (N, D) = Xs.shape
    Z = np.zeros((N-1, 4))
    lastIndex = 0
    for i in range(N-1):
        Z[i,0] = lastIndex
        Z[i,1] = i+1
        Z[i,2] = 0.1 + i
        Z[i,3] = i+2
        lastIndex = N+i
    return Z

def afla_tata(x, tata):
    if tata[x] == x:
        return x
    
    tata[x] = afla_tata(tata[x], tata)
    return tata[x]

def dist(x, y, D):
    d = 0
    for i in range(D):
        d = d + (x[i] - y[i]) * (x[i] - y[i])
    
    return d

def singleLinkage(Xs):
    (N, D) = Xs.shape
    NN = N + N -1
    Z = np.zeros((N-1, 4))
    Dist = np.zeros((NN, NN))
    taken = np.zeros(NN)
    dim = np.zeros(NN)

    for i in range(N):
        dim[i] = 1
    
    for i in range(N):
        for j in range(i + 1, N):
            Dist[i][j] = dist(Xs[i], Xs[j], D)
            Dist[j][i] = Dist[i][j]
            
    for c in range(N-1):
        minim = 999999999
        mini = -1
        minj = -1
        for i in range(N + c):
            for j in range(i + 1, N + c):
                if taken[i] == 0 and taken[j] == 0:
                    k = Dist[i][j]
                    if k < minim:
                        mini = i
                        minj = j
                        minim = k
        
        dim[c + N] = dim[mini] + dim[minj]
        taken[mini] = 1
        taken[minj] = 1
        
        for i in range(N + c):
            Dist[i][N + c] = min(Dist[i][mini], Dist[i][minj])
            Dist[N + c][i] = Dist[i][N + c]
            
        Z[c] = [mini, minj, minim, dim[c + N]]
    return Z

def completeLinkage(Xs):
    (N, D) = Xs.shape
    NN = N + N -1
    Z = np.zeros((N-1, 4))
    Dist = np.zeros((NN, NN))
    taken = np.zeros(NN)
    dim = np.zeros(NN)
    for i in range(N):
        dim[i] = 1
    
    for i in range(N):
        for j in range(i + 1, N):
            Dist[i][j] = dist(Xs[i], Xs[j], D)
            Dist[j][i] = Dist[i][j]
            
    for c in range(N-1):
        minim = 999999999
        mini = -1
        minj = -1
        for i in range(N + c):
            for j in range(i + 1, N + c):
                if taken[i] == 0 and taken[j] == 0:
                    k = Dist[i][j]
                    if k < minim:
                        mini = i
                        minj = j
                        minim = k
        
        dim[c + N] = dim[mini] + dim[minj]
        taken[mini] = 1
        taken[minj] = 1
        
        for i in range(N + c):
            Dist[i][N + c] = max(Dist[i][mini], Dist[i][minj])
            Dist[N + c][i] = Dist[i][N + c]
            
        Z[c] = [mini, minj, minim, dim[c + N]]
    return Z

def groupAverageLinkage(Xs):
    (N, D) = Xs.shape
    NN = N + N -1
    Z = np.zeros((N-1, 4))
    Dist = np.zeros((NN, NN))
    taken = np.zeros(NN)
    dim = np.zeros(NN)
    for i in range(N):
        dim[i] = 1
    
    for i in range(N):
        for j in range(i + 1, N):
            Dist[i][j] = dist(Xs[i], Xs[j], D)
            Dist[j][i] = Dist[i][j]
            
    for c in range(N-1):
        minim = 999999999
        mini = -1
        minj = -1
        for i in range(N + c):
            for j in range(i + 1, N + c):
                if taken[i] == 0 and taken[j] == 0:
                    k = Dist[i][j]
                    if k < minim:
                        mini = i
                        minj = j
                        minim = k
        
        dim[c + N] = dim[mini] + dim[minj]
        taken[mini] = 1
        taken[minj] = 1
        
        for i in range(N + c):
            Dist[i][N + c] = (Dist[i][mini] * dim[i] * dim[mini] + Dist[i][minj] * dim[i] * dim[minj]) / (dim[i] * dim[c + N])
            Dist[N + c][i] = Dist[i][N + c]
            
        Z[c] = [mini, minj, minim, dim[c + N]]
    return Z

def extractClusters(Xs, Z):
    (N, D) = Xs.shape
    assert(Z.shape == (N-1, 4))

    maxim = 0 
    poz = -1
    for i in range(1, N -1):
        if Z[i][2] - Z[i - 1][2] > maxim:
            maxim = Z[i][2] - Z[i - 1][2]
            poz = i
    
    NN = 2 * N - 1
    tata = np.zeros(NN).astype(int)
    for i in range(NN):
        tata[i] = i
        
    for i in range(poz):
        tata[int(Z[i][0])] = i + N
        tata[int(Z[i][1])] = i + N

    for i in range(N):
        tata[i] = afla_tata(i, tata)
        
    dic = {}
    c = -1
    for i in range(N):
        if tata[i] not in dic:
            c = c + 1
            dic[tata[i]] = c

    clusters = np.zeros(N).astype(int)
    for i in range(N):
        clusters[i] = dic[tata[i]]

    return N - poz, clusters

def plot(Xs, K, clusters):

    colors = plt.cm.rainbow(np.linspace(0, 1, K+1))

    if Xs.shape[1] == 2:
        x = Xs[:,0]
        y = Xs[:,1]
        for (_x, _y, _c) in zip(x, y, clusters):
            plt.scatter(_x, _y, s=200, c=colors[_c])
        plt.show()
    elif Xs.shape[1] == 3:
        x = Xs[:,0]
        y = Xs[:,1]
        z = Xs[:,2]
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for (_x, _y, _z, _c) in zip(x, y, z, clusters):
            ax.scatter(_x, _y, _z, s=200, c=colors[_c])
        plt.show()
    else:
        for i in range(len(clusters)):
            print(i, ": ", clusters[i], " ~ ")

def self_cluster_f(Xs,plot_flag = False):
    Z = completeLinkage(Xs)

    plt.figure()
    dn = hierarchy.dendrogram(Z)
    if plot_flag:
        plt.show()

    K, clusters = extractClusters(Xs, Z)
    return clusters

if __name__ == "__main__":

    Xs = np.array([1,2,100,300,30,40,400,200]).reshape(-1,1)
    Z = completeLinkage(Xs)

    plt.figure()
    dn = hierarchy.dendrogram(Z)
    plt.show()

    K, clusters = extractClusters(Xs, Z)

    plot(Xs, K, clusters)

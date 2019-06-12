from sklearn.cluster import KMeans
import numpy as np
import scipy.cluster.hierarchy as hcluster
from self_cluster_fct import self_cluster_f

def self_cluster(col : [int],plot_flag) -> [int]:
    # TODO
    col = np.array(col).reshape(-1,1)
    clusters = self_cluster_f(col,plot_flag)
    print(clusters)
    return clusters

def cluster(n : int, col : [int]) -> [int]:
    col = np.array(col)
    kmeans = KMeans(n_clusters=n, random_state=0).fit(col.reshape(-1,1))
    print(kmeans.labels_)
    return kmeans.labels_

def apply_funct(funct_name : str, args: [str], col : []):
    if funct_name == 'cluster':
        return cluster(int(args[0]),col)
    if funct_name == 'self_cluster':
        return self_cluster(col,bool(args[0]))    
    raise NotImplementedError("unknow function")
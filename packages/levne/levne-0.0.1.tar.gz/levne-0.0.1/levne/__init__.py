from sklearn.preprocessing import normalize
from sklearn import manifold
from sklearn.cluster import KMeans

from matplotlib import pyplot as plt
from matplotlib.lines import Line2D

import numpy
import pandas as pd

import editdistance
import umap
import sys

def reduceDims(chains, reduction='tsne',outputtype = 'numpy'):
    print("Using Levne v0.1 \nA python package for Amino Acid Clustering.\nPublished February 2020 by Christian Šidák.")
    
    #validate inputs:
    if isinstance(chains,pd.core.series.Series):
        chains = chains.tolist()
    elif isinstance(chains,pd.core.frame.DataFrame):
        sys.exit("Error: It looks like you are trying to load in a whole pandas dataframe instead of a column, try chains = df[column] instead.")
    elif not isinstance(chains,list):
        sys.exit("Error: Please input a list pandas Series for your list of amino acid chains")

    #construct N x N distance matrix for N number of chains
    print("Constructing distance matrix...")
    chains2 = chains
    dmatrix = []
    for i in range(len(chains)):
        col = []
        for j in range(len(chains2)):
            dist = editdistance.eval(chains[i],chains2[j])
            col.append(dist)
        dmatrix.append(col)
    dmatrix = numpy.asarray(dmatrix)

    #run TSNE or UMAP
    if reduction == 'tsne':
        print("Running TSNE...")
        model = manifold.TSNE(n_components=2, random_state=0, metric='precomputed')
    elif reduction == 'umap':
        print("Running UMAP...")
        model = umap.UMAP()
    else: 
        sys.exit("Invalid reduction type selected. Valid reduction types are either umap or tsne")
    
    coords = model.fit_transform(dmatrix)

    if outputtype == 'numpy':
        coords = coords
    elif outputtype == 'pandas':
        coords = pd.DataFrame({'chain':chains,'x':coords[:,0],'y':coords[:,1]})
    return(coords)

def findClusters(coords,elbow=0.2,simulations=20):
    Sum_of_squared_distances = []
    K = range(1,simulations)
    marginal_reduction_in_dispersion = 1
    noClusters = 0

    for k in K:
        #simulate clustering at k through K means
        km = KMeans(n_clusters=k)
        km = km.fit(coords)
        Sum_of_squared_distances.append(km.inertia_)

        if k > 1:
            #essentially we are iterating through K means with more and more clusters, 
            #until the marginal percent reduction in sum of squared distances drops below the argument 'elbow'
            marginal_reduction_in_dispersion = Sum_of_squared_distances[k-2]/Sum_of_squared_distances[k-1] - 1
            noClusters = k
            
            if marginal_reduction_in_dispersion< elbow:
                break
    print("Using ",str(noClusters)," clusters...")
    km = KMeans(n_clusters=noClusters)
    km = km.fit(coords)
    return(km.labels_)

def getClusteredDims(chains,reduction='tsne',elbow=0.2,simulations=20):
    coords = reduceDims(chains,reduction=reduction)
    clusters = findClusters(coords,elbow=elbow,simulations=simulations)

    df = pd.DataFrame({
        "chain": chains,
        "x":coords[:,0],
        "y":coords[:,1],
        "cluster":clusters
    })
    return(df)

def drawClusters(chains,reduction='tsne',colorby=[],elbow=0.2,simulations=20,save=True,outdir=None):
    coords = reduceDims(chains,reduction=reduction)
    clusters = findClusters(coords=coords,elbow=elbow,simulations=simulations)
    uniqueClusters = numpy.unique(clusters)

    #pick colors for Cluster Plot
    cmap = plt.get_cmap('tab20') #gets a set of colors from matplotlib
    colors = [cmap(i) for i in numpy.linspace(0, 1, len(uniqueClusters))]
    clusterColorDict = dict(zip(uniqueClusters,colors))
    clusterColorList = [clusterColorDict.get(clusters[i]) for i in range(len(clusters))] #maps points to their color

    #construct scatter plot points FOR CLUSTERS
    print("Making cluster scatterplot...")
    plt.figure(figsize=(7, 7))
    plt.scatter(coords[:, 0], coords[:, 1], marker='o', c=clusterColorList, s=50, edgecolor='None')

    #format legend and chart
    markers = []

    for i in range(len(uniqueClusters)):
        markers.append(Line2D([0], [0], linestyle='None', marker="o", markersize=10, markeredgecolor="none", markerfacecolor=colors[i]))
    lgd = plt.legend(markers, uniqueClusters, numpoints=1, bbox_to_anchor=(1.17, 0.5))
    plt.tight_layout()
    plt.axis('equal')

    df = pd.DataFrame({
        "chain": chains,
        "x":coords[:,0],
        "y":coords[:,1],
        "cluster":clusters
    })

    if len(colorby)>0:
        if isinstance(colorby,pd.core.series.Series):
            colorby = colorby.tolist()
        elif not isinstance(colorby,list):
            sys.exit("Error: please input a list or pandas series as your category to color the scatterplot by.")
        elif len(colorby) !=len(chains):
            sys.exit("Error: you must put in a colorbylist of equal length to the number of sequences you want to visualize.")
        uniqueColors = numpy.unique(colorby)

        colors = [cmap(i) for i in numpy.linspace(0, 1, len(uniqueColors))]
        colorDict = dict(zip(uniqueColors,colors))
        colorList = [colorDict.get(colorby[i]) for i in range(len(colorby))]

        print("Making cluster scatterplot...")
        plt.figure(figsize=(7, 7))
        plt.scatter(coords[:, 0], coords[:, 1], marker='o', c=colorList, s=50, edgecolor='None')

        #format legend and chart
        markers = []

        for i in range(len(uniqueColors)):
            markers.append(Line2D([0], [0], linestyle='None', marker="o", markersize=10, markeredgecolor="none", markerfacecolor=colors[i]))
        lgd = plt.legend(markers, uniqueColors, numpoints=1, bbox_to_anchor=(1.17, 0.5))
        plt.tight_layout()
        plt.axis('equal')
        pngName = str(numpy.random.randint(0,100000))+"_colorbyPlot.png"
        if save:
            if len(outdir)>0:
                pngName = outdir+pngName 
            plt.savefig(pngName)

        df['group'] = colorby

    pngName = str(numpy.random.randint(0,100000))+"_clusterReductionPlot.png"

    if save:
        if len(outdir)>0:
                pngName = outdir+pngName
        plt.savefig(pngName)
    print("Done")
    plt.show()

    return(df)



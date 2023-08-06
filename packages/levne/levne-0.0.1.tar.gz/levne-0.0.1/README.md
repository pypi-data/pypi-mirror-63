# Levne - A package for TCR sequence clustering

Levne is a python package that takes a list of strings, computes a distance matrix using the Levenshtein algorithm, and then runs a dimensionality reduction using either UMAP or TSNE.  Levne also  supports clustering of reduced dimensions using K-means. Published March 2020. 

The package can be used to compare the similar of TCR amino acid sequences, to produce clustering visualizations. Technically, any list of strings can be supplied to levne for distance matrix computation, dimensionality reduction, and clustering, so long as it is formatted as a list or pandas Series.

#### Installation and Requirements

Levne can be installed by running the following bash script from the command line:

```pip install levne```

## Exported Functions
Levne exports four main functions, depending upon the exact kind of output the user wants and how far they want to go in their anaysis. 

#### Reduce Dims
```reduceDims(chains, reduction='tsne',outputtype = 'numpy')```
This function takes a set of strings, constructs a distance matrix based on the Levenshtein algorithm, then reduces the dimensions as either UMAP or TSNE.

Arguments:
```chains```  - the list of strings you want to plot, as either a flat python list or a pandas Series.
```reduction``` - the method of dimensionality reduction you want to use (TSNE or UMAP)
```outputtype``` - 'numpy' to return a numpy array of coordinates, or 'pandas' if you would like to return a pandas dataframe (e.g. for csv export) 

#### Find Clusters
```findClusters(coords,elbow=0.2,simulations=20)```

This function takes in the coordinates output from reduceDims() as a numpy array, then runs K means to cluster the strings based on coordinate position. findClusters will run K means at
1, 2, 3... clusters, going up to the number of clusters specified in the simulations argument. For example, if you set simulations to 10, it will run K means at 1 to 10 clusters, until the marginal 
reduction in the sum of the squared distances (SSD) dips below the percent specified in the elbow argument. For example, let's say you set simulations = 10 and run K means with up to 10 clusters. At 4 clusters,SSD SSD might be 200, then it drops to 150 at 5 clusters. This would be a 25% reduction in SSD. If elbow is set to 0.3, the function would stop and use 5 clusters, because 25% < 0.3. If elbow was 0.1, it would continue on to 6, 7, 8 clusters etc... until the marginal reduction in SSD was below 10%. If SSD reduction does not dip below the elbow parameter between any two neighboring simulations, it will use the max number of clusters set by the simulations parameter.

Arguments:
```coords``` -  a numpy array of coordinates output by reduceDims()
```elbow``` -  the marginal reduction in SSD between simulation of N and M clusters at which you would like to stop simulating K means. Default is 20% (0.2).
```simulations``` - the max number of simulations you would like to run of K means. The first simulation will run with 1 cluster, running up to N clusters until SSD dips below elbow parameter or the number of simulations set by the simulations parameter.

#### Get Clustered Dims
```getClusteredDims(chains,reduction='tsne',elbow=0.2,simulations=20)```

This function calls reduceDims() and findClusters() on a list or pandas series, and returns a dataframe with the x and y coordinates of the dimensionality reduction, along with a cluster annotation.

Arguments:
```chains```  - the list of strings you want to plot, as either a flat python list or a pandas Series.
```reduction``` - the method of dimensionality reduction you want to use (TSNE or UMAP)
```elbow``` -  the marginal reduction in SSD between simulation of N and M clusters at which you would like to stop simulating K means. Default is 20% (0.2).
```simulations``` - the max number of simulations you would like to run of K means. The first simulation will run with 1 cluster, running up to N clusters until SSD dips below elbow parameter or the number of simulations set by the simulations parameter.


#### Draw Clusters
```drawClusters(chains,reduction='tsne',colorby=[],elbow=0.2,simulations=20,save=True,outdir=None)```

This function takes pandas Series or list in the ```chains``` parameter, calls reduceDims() and findClusters(), and then creates a scatterplot of the output using matplotlib, colored by the cluster annotations from the findClusters() parameter. You can also color the dots of the scatterplot by category by supplying a list of strings to the colorby parameter. 

Arguments:
```chains```  - the list of strings you want to plot, as either a flat python list or a pandas Series.
```reduction``` - the method of dimensionality reduction you want to use (TSNE or UMAP)
```colorby``` - a list of strings containing the category annotations for each of your strings in the ```chains``` argument, must be of same lengths as ```chains```
```elbow``` -  the marginal reduction in SSD between simulation of N and M clusters at which you would like to stop simulating K means. Default is 20% (0.2).
```simulations``` - the max number of simulations you would like to run of K means. The first simulation will run with 1 cluster, running up to N clusters until SSD dips below elbow parameter or the number of simulations set by the simulations parameter.
```save``` - a boolean, set to True if you would like save your output pngs.
```outdir``` - the outgoing directory you would like to save your pngs to. 


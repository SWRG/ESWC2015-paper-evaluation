#Evaluation
###Time measurements
The time measurements were taken by running the scripts on a desktop computer having the following characteristics:
* CPU: AMD Phenom II X4 965
* RAM: 12GB DDR3
* OS: Ubuntu Linux 14.04, kernel version: 3.13.0-44-generic

###Node identification
The execution of a query against an RDF-type summary graph consists of three steps: identification of the given typed nodes, calculation of the shortest path between these nodes and conversion of the path to the corresponding SPARQL 1.0 query. The identification step involves retrieving a list of (possibly composite) nodes that contain the given RDF-type and selecting one from this list. Since there is no semantic difference among the nodes in the list we can select any node as long as we use the same node (as an edndpoint) across all RDF-type summary graphs.
For the purposes of the evaluation we have to identify two nodes: one corresponding to the RDF type before the Property Path in the SPARQL 1.1 example query and one corresponding to the RDF type before the Property Path.
###Explanation of the time decrease in the plot
The time measurement depends mainly on the running time of the shortest-path algorithm. Since the 50% dataset contains less triples than the 100% dataset, the corresponding RDF-type summary graphs may contain different shortest paths between the same endpoints. This means that the algorithm would have to examine more nodes (in the RDF-type summary graph of the 50% dataset) in order to find the shortest path. As a result, the query execution time could be greater in the 50% dataset than in the 100% dataset. Therefore, the execution time of the navigational query is independant of the RDF graph size. Instead, it depends on the size of the RDF-type summary which, in turn, is proportional to the number of predicates it contains.
If there is no path between the endpoints, the Dijkstra algorithm is expected to take more time to finish due to visiting a large number of nodes. The complexity is O(V^2)
(proof comming soon)
##Repository Contents
In this repository you can find links to the DBPEDIA datasets that were used for the evaluation of the paper.
###Dataset links
The datasets used for the evaluation can be downloaded from the links below:
* The 100% DBPEDIA dataset: http://benchmark.dbpedia.org/benchmark_100.nt.bz2
* The 50% DBPEDIA dataset: http://benchmark.dbpedia.org/benchmark_50.nt.bz2
* The 10% DBPEDIA dataset: http://benchmark.dbpedia.org/benchmark_10.nt.bz2

The 1% DBPEDIA dataset can be created from the 10% dataset by keeping the first 1537384 triples. This is done by using the head command:

    head -1537384 benchmark_10.nt > benchmark_1.nt

###Automated evaluation script
We have prepared a script that takes as input the 4 DBPEDIA datasets (namely benchmark_1.nt, benchmark_10.nt, benchmark_50.nt and benchmark_100.nt) and creates all RDF-type summary graphs, executes the example query against the graphs, measures execution time and creates the scalability plot. The script can be found at [automated_evaluation.py](https://github.com/SWRG/ESWC2015-paper-evaluation/blob/master/automated_evaluation.py).
Before executing the script make sure networkx and gnuplot are installed in the system. To install these packages on an Ubuntu 14.04 platform, just give the following command:

    sudo apt-get install gnuplot, python-networkx

The dataset files benchmark_1.nt, benchmark_10.nt, benchmark_50.nt and benchmark_100.nt must be in the same directory. The automated evaluation script is executed with the command:

    python automated_evaluation.py DATASET_DIR

where DATASET_DIR is the directory that contains the datasets. The script stores the RDF-type summary graphs in the same directory. In addition, it creates a directory named 'evaluationdata' where it stores the scalability plot along with the corresponding data.
#Evaluation
###Time measurements
The time measurements were taken by running the scripts on a desktop computer having the following characteristics:
* CPU: AMD Phenom II X4 965
* RAM: 12GB DDR3
* OS: Ubuntu Linux 14.04, kernel version: 3.13.0-44-generic

###Querying the RDF-type summary graph
The execution of a query against an RDF-type summary graph consists of three steps:

1. identification of the given typed nodes,
1. calculation of the shortest path between these nodes and
1. conversion of the path to the corresponding SPARQL 1.0 query.

The example query presented in the evaluation section of the paper is this:

    PREFIX dbonto: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/property/>
    SELECT * WHERE {
    ?a a dbonto:MusicalWork.
    ?a ((!a)*/dbp:stylisticOrigins)|(dbp:stylisticOrigins/(!a)*) ?b.
    ?b a dbonto:MusicGenre
    }

In the following paragraphs we give a more thorough analysis of the steps involved in the execution of this query to the RDF-type summary graphs.

###Node identification
The identification step involves retrieving a list of (possibly composite) nodes that contain the given RDF-type and selecting one from this list. Since there is no semantic difference among the nodes in the list, we can select anyone. However, we have to make sure this node exists in every RDF-type summary graph under consideration.

The example SPARQL 1.1 query presented in the evaluation section of the paper contains two RDF types, one in the triple pattern preceding the Property Path (eg. <http://dbpedia.org/ontology/MusicalWork>) and one in the final triple pattern (eg. <http://dbpedia.org/ontology/MusicGenre>). During the identification step, we choose the following common nodes of the RDF-type summary graphs respectively:

* 'http://dbpedia.org/ontology/Album^http://dbpedia.org/ontology/MusicalWork^http://www.w3.org/2002/07/owl#Thing^http://dbpedia.org/ontology/Work'
* 'http://dbpedia.org/class/yago/PunkGenres^http://dbpedia.org/ontology/MusicGenre^http://www.w3.org/2002/07/owl#Thing'

Both of the nodes are composite nodes. The '^' character is used as an RDF type delimiter inside composite nodes. The first node corresponds to <http://dbpedia.org/ontology/MusicalWork>, since it contains the same IRI. The second node corresponds to <http://dbpedia.org/ontology/MusicGenre> for the same reason. Prior to selecting these nodes we made sure they exist in every RDF-type summary graph under consideration.

###Shortest path calculation
After the identification step, a restricted shortest path algorithm is used in order to find the shortest path between the two nodes. The restriction imposed on the algorithm is that either the first or the last edge of a candidate shortest path must be the same as the property contained in the Property Path of the example SPARQL query (eg. <http://dbpedia.org/property/stylisticOrigins>). The algorithm is based on Dijkstra's shortest path algorithm which has a worst case complexity of O(V^2), where V is the number of nodes in the graph.

###Path to SPARQL 1.0 conversion

###Explanation of the time decrease in the plot
The time measurement depends mainly on the running time of the shortest-path algorithm. Since the 50% dataset contains less triples than the 100% dataset, the corresponding RDF-type summary graphs may contain different shortest paths between the same endpoints. This means that the algorithm would have to examine more nodes (in the RDF-type summary graph of the 50% dataset) in order to find the shortest path. As a result, the query execution time could be greater in the 50% dataset than in the 100% dataset. Therefore, the execution time of the navigational query is independant of the RDF graph size. Instead, it depends on the size of the RDF-type summary which, in turn, is proportional to the number of predicates it contains.

If there is no path between the endpoints, the Dijkstra algorithm is expected to take more time to finish due to visiting a greater number of nodes before.

##Repository Contents
In this repository you can find links to the DBPEDIA datasets that were used for the evaluation of the paper.
###Dataset links
The datasets used for the evaluation can be downloaded from the links below:
* The 100% DBPEDIA dataset: http://benchmark.dbpedia.org/benchmark_100.nt.bz2
* The 50% DBPEDIA dataset: http://benchmark.dbpedia.org/benchmark_50.nt.bz2
* The 10% DBPEDIA dataset: http://benchmark.dbpedia.org/benchmark_10.nt.bz2

The 1% DBPEDIA dataset can be created from the 10% dataset by keeping the first 1537384 triples. This is done by executing this command:

    head -1537384 benchmark_10.nt > benchmark_1.nt

###Automated evaluation script
We have prepared a script that takes as input the 4 DBPEDIA datasets (namely benchmark_1.nt, benchmark_10.nt, benchmark_50.nt and benchmark_100.nt) and creates all RDF-type summary graphs, executes the example query against the graphs, measures execution time and creates the scalability plot. The script can be found at [automated_evaluation.py](https://github.com/SWRG/ESWC2015-paper-evaluation/blob/master/automated_evaluation.py).
Before executing the script make sure networkx and gnuplot are installed in the system. To install these packages on an Ubuntu 14.04 platform, just give the following command:

    sudo apt-get install gnuplot, python-networkx

The dataset files benchmark_1.nt, benchmark_10.nt, benchmark_50.nt and benchmark_100.nt must be in the same directory. The automated evaluation script is executed with the command:

    python automated_evaluation.py DATASET_DIR

where DATASET_DIR is the directory that contains the datasets. The script stores the RDF-type summary graphs in the same directory. In addition, it creates a directory named 'evaluationdata' where it stores the scalability plot along with the corresponding data.
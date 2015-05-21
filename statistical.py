# -*- coding: utf-8 -*-
"""
This program reads in a dataset as a N-Ttriples (.nt) file and outputs the
RDF-type degree statistical distribution.

:author: Spyridon Kazanas
:contact: s.kazanas@gmail.com
"""
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from numpy.random import random_sample
import networkx as nx
import random,RDF,argparse,os,sys,csv,cPickle
from operator import itemgetter

rdftype="http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

def plot_hist(x):
    num_bins = 50
    # the histogram of the data
    n, bins, patches = plt.hist(x, num_bins, normed=1, facecolor='green', alpha=0.5)
    # add a 'best fit' line
    #y = mlab.normpdf(bins, mu, sigma)
    #plt.plot(bins, y, 'r--')
    plt.xlabel('Instance Node Degree')
    plt.ylabel('Probability')
    plt.title(r'Histogram of Instance Node Degree of the Host Dataset')

    # Tweak spacing to prevent clipping of ylabel
    plt.subplots_adjust(left=0.15)
    plt.show()

def weighted_values(values, probabilities, size):
    bins = np.add.accumulate(probabilities)
    #print ""
    #print bins
    return values[np.digitize(random_sample(size), bins)]

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog='Example: statistical.py ./input.nt ./output.dat')

    parser.add_argument('input',
                        type=str,
                        metavar='INPUT',
                        help='Dataset (N-Triples file) to be read.')

    parser.add_argument('output',
                        type=str,
                        metavar='CONNECTION',
                        help='Statistical distribution to be output.')

    args = parser.parse_args()

    # Process command line arguments
    input = os.path.abspath(os.path.expanduser(args.input))
    output = os.path.abspath(os.path.expanduser(args.output))

    # Test input file existence
    if not os.path.isfile(input):
        print "Input file not found: ",input
        sys.exit('-1')

    node_degree={}

    # read input and calculate the type degree of every type node
    print "Reading Input dataset."
    for triple in RDF.NTriplesParser().parse_as_stream("file:"+input):
        if str(triple.predicate) == rdftype:
            item = (str(triple.subject),str(triple.predicate),str(triple.object))
            if item[2] not in node_degree:
                node_degree[item[2]] = 0
            node_degree[item[2]] += 1

            if item[2] not in node_degree:
                node_degree[item[2]] = 0
            node_degree[item[2]] += 1

    # Calculate the average type degree of all type nodes
    averagedegree = sum(node_degree.itervalues())/float(len(node_degree))
    maxdegree = max(node_degree.itervalues())
    mindegree = min(node_degree.itervalues())

    print "STATISTICS REPORT"
    print "Min type degree: ",mindegree
    print "Max type degree: ",maxdegree
    print "Average type degree: ",averagedegree
    print ""

    l = sorted([(v,k) for (k,v) in node_degree.iteritems()],reverse=True)

    # Output measured type degrees data
    with open(output, 'wb') as f:
        csvriter = csv.writer(f,delimiter=' ')
        for v,k in l:
            csvriter.writerow([v,k])
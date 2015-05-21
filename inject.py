# -*- coding: utf-8 -*-
"""
This program reads in two N-Ttriples (.nt) files: 
    -the Host Dataset (HD)
    -the Injection Dataset (ID)
and outputs the Connection Dataset (CD) as a N-Triples file.
The Connection Dataset contains ID to HD node connections that match the
average node degree of the HD. The concatenation of HD, ID and CD results to the
final dataset (FD).

Creates log file with CD's report.
Creates plot data file with HD's statistical distriburion.

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
                                     epilog='Example: inject.py ./host.nt ./injection.nt ./connection.nt')

    parser.add_argument('host',
                        type=str,
                        metavar='HOST',
                        help='Host dataset (N-Triples file) to be read.')

    parser.add_argument('injection',
                        type=str,
                        metavar='INJECTION',
                        help='Injection dataset (N-Triples file) to be read.')

    parser.add_argument('connection',
                        type=str,
                        metavar='CONNECTION',
                        help='Connection dataset (N-Triples file) to be output.')

    args = parser.parse_args()

    # Process command line arguments
    host = os.path.abspath(os.path.expanduser(args.host))
    injection = os.path.abspath(os.path.expanduser(args.injection))
    connection = os.path.abspath(os.path.expanduser(args.connection))

    output_dir = os.path.dirname(connection)
    output_file_name = os.path.split(os.path.splitext(connection)[0])[1]

    # Output files
    measured_degree_distribution_file = os.path.join(output_dir,output_file_name+'_measured_degree_distribution.dat')
    measured_degrees_file = os.path.join(output_dir,output_file_name+'_measured_degrees.dat')
    generated_degree_distribution_file = os.path.join(output_dir,output_file_name+'_generated_degree_distribution.dat')
    generated_degrees_file = os.path.join(output_dir,output_file_name+'_generated_degrees.dat')
    logfile = os.path.join(output_dir,output_file_name+'.log')
    reportfile = os.path.join(output_dir,output_file_name+'.REPORT')

    # Test input file existence
    if not os.path.isfile(host):
        print "Input file not found: ",host
        sys.exit('-1')

    if not os.path.isfile(injection):
        print "Input file not found: ",injection
        sys.exit('-1')

    node_degree={}
    predicateset=set()
    hostnodeset=set()

    # read host and calculate the instance degree of every instance node
    print "Reading host dataset."
    for triple in RDF.NTriplesParser().parse_as_stream("file:"+host):
        if str(triple.predicate) != rdftype and not triple.object.is_literal():
            item = (str(triple.subject),str(triple.predicate),str(triple.object))
            if item[0] not in node_degree:
                node_degree[item[0]] = 0
            node_degree[item[0]] += 1

            if item[2] not in node_degree:
                node_degree[item[2]] = 0
            node_degree[item[2]] += 1
            hostnodeset.add(item[0])
            hostnodeset.add(item[2])
            predicateset.add(item[1])

    #counter=collections.Counter(a)
    # Output measured instance degrees data
    with open(measured_degrees_file, 'wb') as f:
        csvriter = csv.writer(f,delimiter=' ')
        for d in node_degree.itervalues():
            csvriter.writerow([d])

    cPickle.dump(node_degree.values(), open(os.path.join(output_dir,output_file_name+'_degrees.p'),'wb'))

    #plot_hist(node_degree.values())
    # Calculate the average instance degree of all instance nodes
    averagedegree = sum(node_degree.itervalues())/float(len(node_degree))
    maxdegree = max(node_degree.itervalues())
    mindegree = min(node_degree.itervalues())

    print "STATISTICS REPORT"
    print "Min instance degree: ",mindegree
    print "Max instance degree: ",maxdegree
    print "Average instance degree: ",averagedegree
    print ""

    with open(reportfile, 'wb') as f:
        f.write("REPORT\n")
        f.write("Host Dataset file: "+host+"\n")
        f.write("Injection Dataset file: "+injection+"\n")
        f.write("Connection Dataset file (output): "+connection+"\n")
        f.write("\n")
        f.write("HOST DATASET STATISTICS \n")
        f.write("Min instance degree: "+str(mindegree)+"\n")
        f.write("Max instance degree: "+str(maxdegree)+"\n")
        f.write("Average instance degree: "+str(averagedegree)+"\n")

    # Calculate instance degree distribution
    degree_count = {}
    total_count = 0
    for n,d in node_degree.iteritems():
        if d not in degree_count:
            # (count,probability)
            degree_count[d] = [0,0.0]
        degree_count[d][0] += 1
        total_count += 1

    total_count_float = float(total_count)
    for d,(c,p) in degree_count.iteritems():
        degree_count[d][1] = c/total_count_float

    v,p = zip(*[(d,p) for d,(c,p) in degree_count.iteritems()])

    values = np.array(v)
    probabilities = np.array(p)

    #cPickle.dump(v, open(os.path.join(output_dir,output_file_name+'_v.p'),'wb'))
    #cPickle.dump(p, open(os.path.join(output_dir,output_file_name+'_p.p'),'wb'))
    cPickle.dump(values, open(os.path.join(output_dir,output_file_name+'_values.p'),'wb'))
    cPickle.dump(probabilities, open(os.path.join(output_dir,output_file_name+'_probabilities.p'),'wb'))

    # output measured instance degree statistical distribution data
    with open(measured_degree_distribution_file, 'wb') as csvfile:
        csvriter = csv.writer(csvfile,delimiter=' ')
        for value,probability in zip(v,p):
            csvriter.writerow([value,probability])

    # read injection dataset
    injnodeset = set()
    print "Reading injection dataset."
    for triple in RDF.NTriplesParser().parse_as_stream("file:"+injection):
        if str(triple.predicate) != rdftype and not triple.object.is_literal():
            item = (str(triple.subject),str(triple.predicate),str(triple.object))
            injnodeset.add(item[0])
            injnodeset.add(item[2])

    injnodelist = list(injnodeset)

    print "Generating Random Degrees"
    # get one random degree for each injection node
    random_degrees = weighted_values(values, probabilities, len(injnodelist))

    # Make connections
    with open(connection,'w') as out:
        # output statistical distribution data
        with open(logfile, 'wb') as csvfile:
            with open(generated_degrees_file, 'wb') as csvfile2:
                csvriter = csv.writer(csvfile,delimiter=' ')
                csvriter2 = csv.writer(csvfile2,delimiter=' ')

                for n,d in zip(injnodelist,random_degrees):
                    print n,", ",d
                    # select d random target nodes from hostnodeset
                    targetnodes = random.sample(hostnodeset, d)

                    # select d random predicates from predicateset
                    predicates = random.sample(predicateset, d)

                    csvriter2.writerow([d])

                    for targetnode,predicate in zip(targetnodes,predicates):

                        # get random edge direction
                        if random.randint(0,1) == 1:
                            # write to Ntriples file
                            out.write('<'+n+'> <'+predicate+'> <'+targetnode+'>'+' .\n')
                            csvriter.writerow([n,predicate,targetnode, 'out'])
                        else:
                            out.write('<'+n+'> <'+predicate+'> <'+targetnode+'>'+' .\n')
                            csvriter.writerow([n,predicate,targetnode, 'in'])
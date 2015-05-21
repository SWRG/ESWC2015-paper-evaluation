"""
This script reads all N-triple files in given directory and then:
1. creates the corresponding RDF-type summary graphs,
2. executes queries against the graphs
3. measures query execution time for each graph
4. creates the scalability plots
5. saves plots and plot-data under the 'evaluationdata' directory

:author: Spyridon Kazanas
:contact: s.kazanas@gmail.com
"""
import os,sys,argparse,csv,imp
from RDFTypeSummary import *

EDGE_FACTOR = 1000000.0

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog='Example: automated_evaluation.py ./datasets')

    parser.add_argument('input_dir',
                        type=str,
                        metavar='INPUT',
                        help='Directory containing datasets as N-Triples files (eg. benchmark_1.nt, benchmark_10.nt, benchmark_50.nt, benchmark_100.nt).')

    args = parser.parse_args()

    # Process command line arguments
    input_dir = os.path.abspath(os.path.expanduser(args.input_dir))
    output_dir = os.path.join(input_dir,'evaluationdata')
    output_file=os.path.join(output_dir,'time')

    # Create dir if it does not exist
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)

    # Check dataset existence
    files_nt=[os.path.join(input_dir,f) for f in files(input_dir) if os.path.splitext(f)[1] =='.nt']
    if len(files_nt)==0:
        print "No N-triples file could be found in: ",input_dir
        print "N-triple file extension should be '.nt'."
        sys.exit('-1')

    # Test gnuplot installation
    if os.system('gnuplot --version') != 0:
        print "Please install gnuplot."
        sys.exit('-1')

    # Test networkx library installation
    try:
        imp.find_module('networkx')
    except ImportError:
        print "Please install Python library: networkx ."
        sys.exit('-1')

    # RDF-type summary creation.
    print "Stage 1: RDF-type summary creation."
    for f in files_nt:
        print "  Processing dataset: ",f
        s = os.system('python create_summary.py '+f)
        if s!=0:
            print "Encountered error."
            sys.exit(-1)

    # Query RDF-type summary.
    print "Stage 2: Executing query against created RDF-type summary graphs."

    # source types
    q_s=frozenset(['S-TYPE'])

    # the property in the property path
    q_p='property'

    # target types
    q_t=frozenset(['T-TYPE'])

    # the limit number
    q_l=10

    # Check graph existence
    files_elist=[os.path.join(input_dir,f) for f in files(input_dir) if os.path.splitext(f)[1] =='.edgelist']
    dataset_percentage_elist=[float(os.path.splitext(os.path.split(f)[1])[0][10:])/100 for f in files_elist]


    if len(files_nt)==0:
        print "No RDF-type summary graphs could be found in: ",input_dir
        sys.exit('-1')

    mysum=RDFTypeSummary()
    results=[]
    for f,dataset_percentage in zip(files_elist,dataset_percentage_elist):
        print "  Querying RDF-type summary graph: ",f
        mysum.loaddb(f)
        result=mysum.execute_query(q_s,q_p,q_t,q_l)
        for i in range(9):
            temp_result=mysum.execute_query(q_s,q_p,q_t,q_l)
            if temp_result[3] < result[3]:
                result = temp_result

        if result[4] is not None:
            print result[4]
            print "(Skipping this result)"
        else:
            # result format: (spql,totalpath,totalpathcost,search_time.total_seconds(),None)
            results.append((result[0],result[1],result[2],result[3],mysum.db_edges,dataset_percentage))

    print "Stage 3: Writing plot data to files"
    print "  (plot data file: ", output_file,")"

    with open(output_file, 'wb') as csvfile:
        csvriter = csv.writer(csvfile,delimiter=' ')
        for r in results:
            csvriter.writerow([r[3],r[4]/EDGE_FACTOR,r[5]])

    print "Stage 3: Plotting data"
    s = os.system('gnuplot -e "filename=\''+output_file+'\'" plot')
    if s!=0:
        print "Encountered error while plotting data. (skipping)"
    print "Finished all evaluation stages."
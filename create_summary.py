# -*- coding: utf-8 -*-
"""
This program creates the RDF-type summary graph by reading triples from
specified N-triples file. The output graph is saved in the same directory.

:author: Spyridon Kazanas
:contact: s.kazanas@gmail.com
"""
import RDF,argparse,os,sys
import networkx as nx

def findtypes(u):
    """
    Finds all rdf-types of input URI (or bnode) u and returns them as a set.

    :param u: Input URI (or bnode)
    :type s: str
    :return: Distinct rdf-types of input URI u.
    :rtype: set
    :requires: list1
    """
    if u not in list1:
        return set()
    return list1[u]

def getunknownname(p):
    if p not in uname:
        serial_num = len(uname)
        name = unknown_class_name + "_" + str(serial_num)
        uname[p] = name
    return uname[p]

# RDF type delimiter in composite nodes
tdelimiter='^'

unknown_class_name="unknown"
rdftype="http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
uname = dict()
list1={}

# final graph
g = nx.MultiDiGraph()

# substitutions_dict[(st,p,ot)] = number_of_replaced_triples
substitutions_dict = dict()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog='Example: dataloader.py ./input.nt')    

    parser.add_argument('inputfile',
                        type=str,
                        metavar='INPUT',
                        help='N-Triples file to be read.')

    args = parser.parse_args()

    # Process command line arguments
    inputfile = os.path.abspath(os.path.expanduser(args.inputfile))

    # Test input file existence
    if not os.path.isfile(inputfile):
        print "Input file not found: ",inputfile
        sys.exit('-1')

    output_dir = os.path.dirname(os.path.abspath(os.path.expanduser(args.inputfile)))
    output_file = os.path.join(output_dir,os.path.split(os.path.splitext(inputfile)[0])[1]+'.edgelist')

    # First Pass: Type dictionary creation.
    ERDF=0
    print "First Pass: Type dictionary creation."
    for triple in RDF.NTriplesParser().parse_as_stream("file:"+inputfile):
        ERDF+=1
        if str(triple.predicate) == rdftype:
            s=str(triple.subject)
            if s in list1:
                list1[s].add(str(triple.object))
            else:
                list1[s]=set()
                list1[s].add(str(triple.object))

    # Second Pass: Graph creation.
    print "Second Pass: Graph creation."
    for triple in RDF.NTriplesParser().parse_as_stream("file:"+inputfile):
        if str(triple.predicate) != rdftype and not triple.object.is_literal():
            item = (str(triple.subject),str(triple.predicate),str(triple.object))

            # Subject types
            st_set = findtypes(item[0])
            len_st_set = len(st_set)
            if (len_st_set == 0):
                # if no type found, put it to the default unknown type
                st = getunknownname(item[1])
            elif (len_st_set == 1):
                # If single type found, use it as the replacement
                st = list(st_set)[0]
            elif (len_st_set > 1):
                # If there are more than one types, create the composite 
                # type as a concatenation
                st = tdelimiter.join(st_set)

            # Object types
            ot_set = findtypes(item[2])
            len_ot_set = len(ot_set)
            if (len_ot_set == 0):
                #if no type found, put it to the default unknown type
                ot = getunknownname(item[1])
            elif (len_ot_set == 1):
                # If single type found, use it as the replacement 
                ot = list(ot_set)[0]
            elif (len_ot_set > 1):
                # If there are more than one types, create the composite 
                # type as a concatenation
                ot = tdelimiter.join(ot_set)

            key = (st, item[1], ot)
            if key not in substitutions_dict:
                substitutions_dict[key] = 0
            substitutions_dict[key]+=1

    del list1

    # Weighting Step
    print "Weighting."
    NR_int=sum((substitutions_dict[k] for k in substitutions_dict))
    NR=float(NR_int)
    N=float(len(substitutions_dict))

    # Add substitutions from the dict
    for (st,p,ot) in substitutions_dict:
        Nc=substitutions_dict[(st,p,ot)]
        Ws=(1+(1-Nc/NR)/(N-1))/(N+1)
        g.add_edge(st,ot,p,{'label':p,'weight':Ws})

    # save data
    print "Saving data."
    nx.write_edgelist(g, open(output_file,'wb'), data=True)

    # Report
    print "REPORT"
    print "  ORIGINAL RDF:"
    print "    Total RDF Edges |E_RDF|=",ERDF
    print "    Total RDF Connection Edges |E_2|=",NR_int
    print ""
    print "  RDF-TYPE SUMMARY:"
    print "    Total Nodes |N_S|=",len(g.nodes())
    print "    Total Edges |E_S|=",len(g.edges())
    print "    Total Weight Sum(W_S)=",sum((e[2]['weight'] for e in g.edges_iter(data=True)))


    print "RDF-type summary graph file created: " + output_file
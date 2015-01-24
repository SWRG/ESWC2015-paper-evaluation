# -*- coding: utf-8 -*-
"""
This class can be used to load an RDF-type summary graph and execute queries
against it. The graph may be stored either in Pickle format or as an edge list.

:author: Spyridon Kazanas
:contact: s.kazanas@gmail.com
"""
import datetime
import networkx as nx
from corefunctions import get_sparql_from_graph
from dijkstra import *
from parser import *
from cPickle import load, dump
from os import path

class RDFTypeSummary():
    # db info
    db_graph = None
    db_file = None
    db_nodes = None
    db_edges = None
    db_weight = None
    tdelimiter = None

    def __init__(self,inputfile=None,tdelimiter='^'):
        self.tdelimiter=tdelimiter
        if inputfile is not None:
            self.loaddb(inputfile)

    def loaddb(self,inputfile):
        """
        Loads db_graph, shortest path data and labelings from save directory.
        Sorts labelings.

        :param dirpath: The directory containing data.
        """
        inputfile = path.abspath(path.expanduser(inputfile))

        print "Loading RDF-type summary graph: ",inputfile
        print "(please wait)"

        if path.isfile(inputfile):
            self.unloaddb()
            self.db_graph = read_edgelist_2(inputfile,comments=" //#",nodetype=str,create_using=nx.MultiDiGraph())
        else:
            print "File not found."
            return
        self.db_file = inputfile
        self.db_nodes = len(self.db_graph.nodes())
        self.db_edges = len(self.db_graph.edges())
        self.db_weight = self.db_graph.size(weight='weight')
        self.dbinfo()
        print "Done loading."
        return

    def unloaddb(self):
        self.db_graph = None
        self.db_file = None
        self.db_nodes = None
        self.db_edges = None
        self.db_weight = None

    def dbinfo(self):
        print "Database information:"
        print "    File : ",self.db_file
        print "    Nodes: ",self.db_nodes
        print "    Edges: ",self.db_edges
        print "    Total weight: ",self.db_weight
        return

    def execute_query(self,q_source,q_predicate,q_target):
        '''Queries db and returns results.
        '''
        search_time = datetime.datetime.now()

        print "Executing query:"
        print q_source,q_predicate,q_target


        # find q_predicate that touches q_source
        ets=[(e[0],e[2]['label'],e[1]) for e in self.db_graph.out_edges_iter([q_source],data=True, keys=False)]

        # find inner node for each edge
        nts=[v[2] for v in ets]
        nts_p=[v[1] for v in ets]

        # find q_predicate that touches q_target
        ett=[(e[0],e[2]['label'],e[1]) for e in self.db_graph.in_edges_iter([q_target],data=True, keys=False)]

        # find inner node for each edge
        ntt=[v[0] for v in ett]
        ntt_p=[v[1] for v in ett]

        minshpath=None
        # Choose the shortest of the paths that connect each node of nts to each node of ntt
        for na,na_p in zip(nts,nts_p):
            FINISH_FLAG = False
            minshpath=None
            minshpath_l=None
            for nb,nb_p in zip(ntt,ntt_p):
                # predicate must be in at least 1 endpoint
                if na_p != q_predicate and nb_p != q_predicate: continue

                try:
                    print "trying: ",(na_p,na),(nb,nb_p)
                    shpath_l,shpath=dijkstra_path_2(self.db_graph, na, nb,weight='weight')
                    print "done"
                except:
                    print "failed"
                    continue
                if not minshpath or shpath_l<minshpath:
                    # Minimum path
                    minshpath=shpath
                    minshpath_l=shpath_l

                    # Determine final inner nodes nis and nit.
                    nis=na
                    nis_p=na_p
                    nit=nb
                    nit_p=nb_p
                    print nis
                    print nit

                    # Get the weights of these 2 edges
                    nisw=self.db_graph[q_source][nis][nis_p]['weight']
                    nitw=self.db_graph[nit][q_target][nit_p]['weight']
                    FINISH_FLAG = True
                    break
            if FINISH_FLAG: break

        if not minshpath:
            print "No connectivity between given RDF types."
            return None,None,None,None,"No connectivity between given RDF types."

        totalpath=[q_source,(q_source,nis_p,nis)]+minshpath+[(nit,nit_p,q_target),q_target]
        totalpathcost=nisw+nitw+minshpath_l

        # Generate SPARQL for path.
        spql = get_sparql_from_graph(totalpath,tdelimiter=self.tdelimiter)

        # duration of query processing
        search_time = datetime.datetime.now() - search_time

        return spql,totalpath,totalpathcost,search_time.total_seconds(),None
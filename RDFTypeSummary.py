# -*- coding: utf-8 -*-
"""
This class can be used to load an RDF-type summary graph and execute queries
against it. The graph is stored as an edge list file.

:author: Spyridon Kazanas
:contact: s.kazanas@gmail.com
"""
import datetime,requests,json,csv
import networkx as nx
from corefunctions import *
from dijkstra import *
from parser import *
import cPickle
from os import path
from networkx.classes.multidigraph import MultiDiGraph
import itertools

class RDFTypeSummary():
    # db info
    db_graph = None
    db_file = None
    db_nodes = None
    db_edges = None
    db_weight = None

    def __init__(self,inputfile=None):
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
            self.db_graph=MultiDiGraph()
            with open(inputfile,"rb") as f:
                csvreader=csv.reader(f,delimiter=' ')
                self.db_graph.add_edges_from((cPickle.loads(row[0]) for row in csvreader))
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

    def execute_query2(self,q_source,q_predicate,q_target,q_limit,endpoint='http://localhost:8890/sparql'):
        '''Queries db and returns results.
        '''
        search_time = datetime.datetime.now()

        print "Executing query:"
        print q_source,q_predicate,q_target

        types_query=""
        for i in q_source:
            types_query+="?_a a <"+i+">."
        for i in q_target:
            types_query+="?_b a <"+i+">."

        info_list=[]
        remainingresults = q_limit
        results_sorted=[]
        resutset=set()
        ask_time_total=0.0 # measures total ask time
        select_time_total=0.0 # measures total ask time
        cur_path_length=0
        while remainingresults > 0:
            counter = itertools.count()

            print "Path Length=",cur_path_length

            query="{"
            query+=types_query

            query+="?_a"
            for i in range(cur_path_length):
                var="?_"+str(cur_path_length)+"_"+str(i)
                query+=" !a "+var+"."+var
            query+=" <"+q_predicate+"> ?_b.}"

            ask_query="ASK "+query
            select_query="SELECT DISTINCT ?_a ?_b WHERE "+query

            # execute ASK query
            has_results=None

            # time ASK query
            print 'ASK'
            #print "    ",ask_query
            time_ask = datetime.datetime.now()
            has_results=requests.post(endpoint,{'timeout':'0','format':'text/plain','query': ask_query})
            time_ask = datetime.datetime.now()-time_ask
            time_ask=time_ask.total_seconds()
            ask_time_total+=time_ask

            print "has_results=",has_results.text
            if has_results.text=="true":
                # execute SELECT query
                results=None

                # time SELECT query
                print 'SELECT'
                print "    ",select_query
                time_select = datetime.datetime.now()
                results=requests.post(endpoint,{'timeout':'0','format':'application/sparql-results+json','query': select_query})
                time_select = datetime.datetime.now()-time_select
                time_select=time_select.total_seconds()
                select_time_total+=time_select

                results_dict=json.loads(results.text)
                print "Results=",results_dict

                # count results
                results_number = len(results_dict['results']['bindings'])
                print "Results number=",results_number
                print "Remaining results=",remainingresults

                if results_number >=remainingresults:
                    #add limit to the last select query: LIMIT remainingresults
                    select_query+='LIMIT '+str(remainingresults)

                    # append query
                    info_list.append((cur_path_length,select_query,ask_query,time_ask,time_select))
                    print "Limit reached, breaking"
                    break   # q_limit reached
                else:
                    # append query
                    info_list.append((cur_path_length,select_query,ask_query,time_ask,time_select))
                    remainingresults-=results_number
                    print "Limit not reached, continuing, remaining results=",remainingresults
            cur_path_length+=1
        if not info_list:
            print "No connectivity between given RDF types."
            return None,None,None,None,None,"No connectivity between given RDF types."
        else:
            COMBINED_SELECT_SPARQL="SELECT * {"
            for row in info_list:
                COMBINED_SELECT_SPARQL+="{"+row[1]+"}UNION"
            COMBINED_SELECT_SPARQL=COMBINED_SELECT_SPARQL[:-5]+"}"

            # duration of query processing
            search_time = datetime.datetime.now()-search_time
            search_time=search_time.total_seconds()
            print COMBINED_SELECT_SPARQL
            # COMBINED_SELECT_SPARQL,PATHS,PATH_LENGTHS,TIME_ASK,TIME_SELECT,TOTAL_TIME
            return COMBINED_SELECT_SPARQL,info_list,ask_time_total,select_time_total,search_time,None

    def execute_query(self,q_source,q_predicate,q_target,q_limit,endpoint='http://localhost:8890/sparql'):
        '''Queries db and returns results.
        '''
        search_time = datetime.datetime.now()

        print "Executing query:"
        print q_source,q_predicate,q_target

        # blacklist of edges in the form (n1,p,n2)
        g_source_removed=set([(e[0],e[2],e[1]) for e in self.db_graph.out_edges_iter([q_source],data=False, keys=True) if e[2] != q_predicate])
        g_target_removed=set([(e[0],e[2],e[1]) for e in self.db_graph.in_edges_iter([q_target],data=False, keys=True) if e[2] == q_predicate])
        g_source_removed2=set([(e[0],e[2],e[1]) for e in self.db_graph.out_edges_iter([q_source],data=False, keys=True) if e[2] == q_predicate])
        g_target_removed2=set([(e[0],e[2],e[1]) for e in self.db_graph.in_edges_iter([q_target],data=False, keys=True) if e[2] != q_predicate])

        pathgen1 = YenKSP_generator(self.db_graph,q_source,q_target,g_source_removed|g_target_removed)
        pathgen2 = YenKSP_generator(self.db_graph,q_source,q_target,g_source_removed2|g_target_removed2)

        generators=[pathgen1,pathgen2]
        generatedvalues=[]

        for g in generators:
            try:
                length,path=g.next()
                heappush(generatedvalues, (length,(path,g)))
            except StopIteration:
                print 'Generator finished: ',g
                pass

        info_list=[]
        remainingresults = q_limit
        results_sorted=[]
        resultset=set()
        ask_time_total=0.0 # measures total ask time
        select_time_total=0.0 # measures total ask time
        while generatedvalues:
            print "****************************************"
            # get new shortest path
            curlength,(curspath,curpathgen)=heappop(generatedvalues)

            #do job
            print "Using generator: ",curpathgen
            print "Path Length: ",curlength
            print "Path : ",curspath

            assert curspath[-2][1]==q_predicate
            assert curspath[0]==q_source
            assert curspath[-1]==q_target

            # integer path length (edge count)
            int_path_length=len(curspath)/2
            print "Int Path length: ",int_path_length

            #convert spath to an ASK query and a SELECT query
            ask_query,select_query,last_var = get_sparql_from_path(curspath)

            # execute ASK query
            has_results=None

            # time ASK query
            print 'ASK'
            print "    ",ask_query
            time_ask = datetime.datetime.now()
            has_results=requests.post(endpoint,{'timeout':'0','format':'text/plain','query': ask_query})
            time_ask = datetime.datetime.now()-time_ask
            time_ask=time_ask.total_seconds()
            ask_time_total+=time_ask

            print "has_results=",has_results.text
            if has_results.text=="true":
                # execute SELECT query
                results=None

                # time SELECT query
                print 'SELECT'
                print "    ",select_query
                time_select = datetime.datetime.now()
                results=requests.post(endpoint,{'timeout':'0','format':'application/sparql-results+json','query': select_query})
                time_select = datetime.datetime.now()-time_select
                time_select=time_select.total_seconds()
                select_time_total+=time_select

                results_dict=json.loads(results.text)

                # Results of this select query (may contain less unique results).
                cur_results=[(b['_1']['value'],b[last_var[1:]]['value']) for b in results_dict['results']['bindings']]

                # add results to list and mark last index for the limit
                limit=0
                for i,r in enumerate(cur_results):
                    print "results_sorted: ",results_sorted
                    print "resultset: ",resultset
                    print "current result:",r
                    if r not in resultset:
                        results_sorted.append((int_path_length,r[0],r[1]))
                        resultset.add(r)
                        limit=i+1
                        remainingresults-=1
                        if remainingresults==0:
                            #add limit to the last select query: LIMIT remainingresults
                            select_query+='LIMIT '+str(limit)

                            # append query
                            info_list.append((curspath,curlength,select_query,ask_query,time_ask,time_select))
                            print "Limit reached, breaking"
                            break

                if remainingresults==0:
                    print "Limit reached, breaking"
                    break
                else:
                    print "Limit not reached, continuing, remaining results=",remainingresults

            # advance
            try:
                curlength,curpath=curpathgen.next()
                heappush(generatedvalues, (curlength,(curpath,curpathgen)))
            except StopIteration:
                print 'Generator finished: ',curpathgen

        if not info_list:
            print "No connectivity between given RDF types."
            return None,None,None,None,None,"No connectivity between given RDF types."
        else:
            COMBINED_SELECT_SPARQL="SELECT * {"
            for row in info_list:
                COMBINED_SELECT_SPARQL+="{"+row[2]+"}UNION"
            COMBINED_SELECT_SPARQL=COMBINED_SELECT_SPARQL[:-5]+"}"

            # duration of query processing
            search_time = datetime.datetime.now()-search_time
            search_time=search_time.total_seconds()
            print COMBINED_SELECT_SPARQL
            # COMBINED_SELECT_SPARQL,PATHS,PATH_LENGTHS,TIME_ASK,TIME_SELECT,TOTAL_TIME
            return COMBINED_SELECT_SPARQL,info_list,ask_time_total,select_time_total,search_time,None

# -*- coding: utf-8 -*-
"""
This library contains various needed functions.

:author: Spyridon Kazanas
:contact: s.kazanas@gmail.com
"""
import networkx as nx
from dijkstra import *

def split_composite(n,tdelimiter):
    if tdelimiter in n:
        return tuple(n.split(tdelimiter))
    return tuple([n])

def types_from_node(n,tdelimiter):
    return tuple(split_composite(n,tdelimiter))

def is_pnode(node):
    if type(node) is tuple:
        return True
    return False

def is_unknown(n):
    if "unknown_" in n or n == "unknown":
        return True
    return False

def get_shortest_path(Graph,source,sink):
    """
    Returns the shortest path from source node to sink node in Graph.

    :param Graph: The graph to be searched.
    :type Graph: nx.Graph()
    :param source: Starting node.
    :param sink: Ending node.
    :return: The shortest path as a list of nodes and edges. Endnodes are included.
    :rtype: list
    """

    try:
        path = dijkstra_path_2(Graph, source, sink)
        return path
    except:
        return None

def is_equal(g1,g2):
    """Returns True if both graphs are identical."""
    return g1.adj == g2.adj

def get_sparql_from_graph(treegraph,tdelimiter):
    '''
    Graph to SPARQL converter.

    :param treegraph: The graph to be converted to sparql.
    :returns: A string with SPARQL code.
    '''

    def add_triple_pattern(sparql_var,rdf_type):
        if sparql_var not in added_patterns:
            added_patterns[sparql_var] = set()
        added_patterns[sparql_var].add(rdf_type)
        return

    def add_conn_pattern(sparql_var_1,predicate,sparql_var_2):
        if (sparql_var_1,sparql_var_2) not in added_conn_patterns:
            added_conn_patterns[(sparql_var_1,sparql_var_2)] = set()
        added_conn_patterns[(sparql_var_1,sparql_var_2)].add(predicate)
        return

    added_patterns = {}
    added_conn_patterns = {}
    sn=1
    for pnode in treegraph:
        if not is_pnode(pnode): continue

        (source,predicate,target) = pnode
        s_var="?_"+str(sn)
        sn+=1
        t_var="?_"+str(sn)

        # extract simple rdf types from composites
        sources = list(types_from_node(source,tdelimiter))
        targets = list(types_from_node(target,tdelimiter))

        for s in sources: 
            if not is_unknown(s):
                add_triple_pattern(s_var,s)

        for t in targets:
            if not is_unknown(t):
                add_triple_pattern(t_var,t)

        # connect s_var to t_var with predicate
        add_conn_pattern(s_var,predicate,t_var)

    # string to be filled with sparql triple patterns
    triplepatterns = ""

    # concatenate rdf type triple patterns
    for sparl_var in added_patterns:
        rdftypes = added_patterns[sparl_var]
        for rdftype in rdftypes:
            triplepatterns += sparl_var + " a <" + rdftype + "> .\n"

    # concatenate subject to object connection triple patterns
    for (sparl_var_1,sparl_var_2) in added_conn_patterns:
        predicates = added_conn_patterns[(sparl_var_1,sparl_var_2)]
        for predicate in predicates:
            triplepatterns +=  sparl_var_1 + " <" + predicate + "> " + sparl_var_2 + " .\n"

    # we are going to use select *
    var_str = "*"

    querystr = "".join([
                "SELECT DISTINCT " + var_str + " WHERE {\n",
                triplepatterns,
                "}"])

    return querystr
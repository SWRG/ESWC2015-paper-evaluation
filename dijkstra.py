# -*- coding: utf-8 -*-
"""
Minor changes to the original Networkx functions. The shortest path is defined
as a list of nodes and edges.

Example:
g = nx.MultiDiGraph()
g.add_edge('1','2','p1',{'label':'p1','weight':0.2})
g.add_edge('1','2','p2',{'label':'p2','weight':0.1})
g.add_edge('1','2','p3',{'label':'p3','weight':0.3})
g.add_edge('0','1','p3',{'label':'p3','weight':0.3})
g.add_edge('2','3','p2',{'label':'p2','weight':0.1})

In [8]: dijkstra_path_2(g,'0','3','weight')
Out[8]: 
(0.5,
 ['0', ('0', 'p3', '1'), '1', ('1', 'p2', '2'), '2', ('2', 'p2', '3'), '3'])


Example 2:
from corefunctions import *
g = nx.MultiDiGraph()
g.add_edge('1','2','p1',{'label':'p1','weight':0.2})
g.add_edge('1','2','p2',{'label':'p2','weight':0.2})
g.add_edge('1','2','p3',{'label':'p3','weight':0.2})
g.add_edge('1','3','p7',{'label':'p7','weight':0.2})
g.add_edge('1','4','p2',{'label':'p2','weight':0.2})
g.add_edge('1','4','p1',{'label':'p1','weight':0.2})
g.add_edge('1','5','p2',{'label':'p2','weight':0.2})

g.add_edge('2','3','p2',{'label':'p2','weight':0.2})
g.add_edge('2','3','p3',{'label':'p3','weight':0.2})
g.add_edge('2','4','p4',{'label':'p4','weight':0.2})
g.add_edge('2','4','p5',{'label':'p5','weight':0.2})

g.add_edge('3','1','p2',{'label':'p2','weight':0.2})
g.add_edge('3','5','p1',{'label':'p1','weight':0.2})
g.add_edge('3','5','p6',{'label':'p6','weight':0.2})

pg=YenKSP_generator(g,'1','3',set(),'p2')
pg.next()


from corefunctions import *
g1 = nx.MultiDiGraph()

g1.add_edge('1','2','p1',{'label':'p1','weight':0.1})
g1.add_edge('2','3','p2',{'label':'p2','weight':0.2})
g1.add_edge('3','3','p',{'label':'p','weight':0.3})

g2 = nx.MultiDiGraph()
g2.add_edge('1','2','p1',{'label':'p1','weight':0.1})
g2.add_edge('2','3','p2',{'label':'p2','weight':0.2})
g2.add_edge('3','4','p',{'label':'p','weight':0.3})

g3 = nx.MultiDiGraph()
g3.add_edge('1','2','p1',{'label':'p1','weight':0.1})
g3.add_edge('2','3','p2',{'label':'p2','weight':0.2})
g3.add_edge('3','4','p',{'label':'p','weight':0.3})
g3.add_edge('3','2','p3',{'label':'p3','weight':0.3})

g4 = nx.MultiDiGraph()
g4.add_edge('1','2','p1',{'label':'p1','weight':0.1})
g4.add_edge('2','3','p2',{'label':'p2','weight':0.2})
g4.add_edge('3','4','p',{'label':'p','weight':0.3})
g4.add_edge('3','2','p3',{'label':'p3','weight':0.3})
g4.add_edge('2','3','p4',{'label':'p4','weight':0.3})

:author: Spyridon Kazanas
:contact: s.kazanas@gmail.com
"""
import networkx as nx
import heapq,itertools

def single_source_dijkstra_2(G,source,target=None,cutoff=None,blacklist=set(),weight='weight'):
    '''
    blacklist=set([(n1,p,n2)])
    It is a set of edges in the form of tuple (node1,predicate,node2)
    '''
    counter = itertools.count()
    if source==target:
        return ({source:0}, {source:[source]})
    dist = {}  # dictionary of final distances
    paths = {source:[source]}  # dictionary of paths

    epaths={source:[source]}

    seen = {source:0}
    fringe=[] # use heapq with (distance,label) tuples
    heapq.heappush(fringe,(0,next(counter),source))
    while fringe:
        (d,count,v)=heapq.heappop(fringe)
        if v in dist:
            continue # already searched this node.
        dist[v] = d
        if v == target:
            break

        edata=[]
        for w,keydata in G[v].items():
            #find minimum weight edge
            minweightlabel=(float('Inf'),None)
            for k,dd in keydata.items():
                if (v,k,w) not in blacklist:
                    curweight=dd[weight]
                    if curweight < minweightlabel[0]:
                        minweightlabel=(curweight,k) 
            #try:
                #minweightlabel=min(((dd.get(weight,1),k) for k,dd in keydata.items() if (v,k,w) not in blacklist))
                #minweightlabel=min(((dd['weight'],k) for k,dd in keydata.items() if (v,k,w) not in blacklist))
                
            #except ValueError:
                #continue
            if minweightlabel[1] is not None:
                edata.append((w,{weight:minweightlabel[0],'label':minweightlabel[1]}))

        for w,edgedata in edata:
            vw_dist = dist[v] + edgedata.get(weight,1)
            if cutoff is not None:
                if vw_dist>cutoff:
                    continue
            if w in dist:
                if vw_dist < dist[w]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif w not in seen or vw_dist < seen[w]:
                seen[w] = vw_dist
                heapq.heappush(fringe,(vw_dist,next(counter),w))
                paths[w] = paths[v]+[w]

                epaths[w] = epaths[v]+[(v,edgedata['label'],w)]+[w]
    return (dist,epaths)

def dijkstra_path_2(G, source, target, blacklist, weight):
    (length,path)=single_source_dijkstra_2(G, source, target=target,blacklist=blacklist,weight=weight)
    try:
        return length[target],path[target]
    except KeyError:
        raise nx.NetworkXNoPath("node %s not reachable from %s"%(source,target))
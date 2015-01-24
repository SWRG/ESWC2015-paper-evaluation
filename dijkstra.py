# -*- coding: utf-8 -*-
"""
Minor changes to the original Networkx functions. The shortest path is defined
as a list of nodes and edges.

Example:
g.add_edge('1','2','p1',{'label':'p1','weight':0.2})
g.add_edge('1','2','p2',{'label':'p2','weight':0.1})
g.add_edge('1','2','p3',{'label':'p3','weight':0.3})
g.add_edge('0','1','p3',{'label':'p3','weight':0.3})
g.add_edge('2','3','p2',{'label':'p2','weight':0.1})

In [30]: dijkstra_path_2(g,'0','3','weight')
Out[30]: ['0', ('0', 'p3', '1'), '1', ('1', 'p2', '2'), '2', ('2', 'p2', '3'), '3']

:author: Spyridon Kazanas
:contact: s.kazanas@gmail.com
"""
import networkx as nx
import heapq

def single_source_dijkstra_2(G,source,target=None,cutoff=None,weight='weight'):
    if source==target:
        return ({source:0}, {source:[source]})
    dist = {}  # dictionary of final distances
    paths = {source:[source]}  # dictionary of paths
    
    epaths={source:[source]}
    
    seen = {source:0}
    fringe=[] # use heapq with (distance,label) tuples
    heapq.heappush(fringe,(0,source))
    while fringe:
        (d,v)=heapq.heappop(fringe)
        if v in dist:
            continue # already searched this node.
        dist[v] = d
        if v == target:
            break

        edata=[]
        for w,keydata in G[v].items():
            minweightlabel=min(((dd.get(weight,1),dd['label']) for k,dd in keydata.items()))
            #minweight=min((dd.get(weight,1) for k,dd in keydata.items()))
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
                heapq.heappush(fringe,(vw_dist,w))
                paths[w] = paths[v]+[w]

                epaths[w] = epaths[v]+[(v,edgedata['label'],w)]+[w]
    return (dist,epaths)

def dijkstra_path_2(G, source, target, weight):
    (length,path)=single_source_dijkstra_2(G, source, target=target,weight=weight)
    try:
        return length[target],path[target]
    except KeyError:
        raise nx.NetworkXNoPath("node %s not reachable from %s"%(source,target))
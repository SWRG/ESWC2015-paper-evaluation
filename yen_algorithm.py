def get_path_length(G, path, weight='weight'):
    length = 0
    if len(path) > 1:
        for i in range(1,len(path),2):
            u,p,v = path[i]
            length += G[u][v][p][weight]
    return length

def YenKSP_generator(Graph, source, sink, blacklist, weight='weight'):
    """
    Makes an iterator that returns shortest paths ordered by ascending path 
    weight. 

    This is an implementation of Yen's K-Shortest Paths Algorithm, based on 
    Antonin Lenfant's work for the igraph library (see https://gist.github.com/ALenfant)

    :param inGraph: The graph to be searched.
    :type inGraph: networkx.MultiDiGraph()
    :param source: Starting node.
    :param sink: Ending node.
    :param weight: The key in edge's attribute dict corresponding to edge weights.
    :return: Tuples that contain a path and it's weight as: (weight,path)
    :rtype: tuple

    Example:
    In [103]: edges=[(1, 2, 'p2', {'weight': 0.2, 'label':'p2'}),
       .....:  (1, 2, 'p3', {'weight': 0.3, 'label':'p3'}),
       .....:  (1, 2, 'p1', {'weight': 0.1, 'label':'p1'}),
       .....:  (2, 1, 'p3', {'weight': 0.21, 'label':'p3'}),
       .....:  (2, 3, 'p4', {'weight': 0.21, 'label':'p4'}),
       .....:  (2, 3, 'p5', {'weight': 0.421, 'label':'p5'}),
       .....:  (3, 4, 'p6', {'weight': 0.6, 'label':'p6'}),
       .....:  (4, 9, 'p1', {'weight': 1.6, 'label':'p1'}),
       .....:  (9, 8, 'p2', {'weight': 1.6, 'label':'p2'}),
       .....:  (3, 5, 'p7', {'weight': 0.3, 'label':'p7'}),
       .....:  (3, 6, 'p7', {'weight': 0.1, 'label':'p7'}),
       .....:  (5, 8, 'p3', {'weight': 0.4, 'label':'p3'}),
       .....:  (6, 1, 'p1', {'weight': 0.1, 'label':'p1'})]

    In [104]: 

    In [104]: G=nx.MultiDiGraph()

    In [105]: 

    In [105]: for e in edges:
       .....:         G.add_edge(e[0],e[1],e[2],e[3])
       .....:     

    In [106]: gen=YenKSP_generator(G,1,1)

    In [107]: [p for p in gen]
    Out[107]: [(0, [1])]

    In [108]: gen=YenKSP_generator(G,1,2)

    In [109]: [p for p in gen]
    Out[109]: 
    [(0.1, [1, (1, 'p1', 2), 2]),
     (0.2, [1, (1, 'p2', 2), 2]),
     (0.3, [1, (1, 'p3', 2), 2])]

    In [110]: gen=YenKSP_generator(G,1,8)

    In [111]: [p for p in gen]
    Out[111]: 
    [(1.01,
      [1, (1, 'p1', 2), 2, (2, 'p4', 3), 3, (3, 'p7', 5), 5, (5, 'p3', 8), 8]),
     (1.1099999999999999,
      [1, (1, 'p2', 2), 2, (2, 'p4', 3), 3, (3, 'p7', 5), 5, (5, 'p3', 8), 8]),
     (1.21,
      [1, (1, 'p3', 2), 2, (2, 'p4', 3), 3, (3, 'p7', 5), 5, (5, 'p3', 8), 8]),
     (1.221,
      [1, (1, 'p1', 2), 2, (2, 'p5', 3), 3, (3, 'p7', 5), 5, (5, 'p3', 8), 8]),
     (1.321,
      [1, (1, 'p2', 2), 2, (2, 'p5', 3), 3, (3, 'p7', 5), 5, (5, 'p3', 8), 8]),
     (1.421,
      [1, (1, 'p3', 2), 2, (2, 'p5', 3), 3, (3, 'p7', 5), 5, (5, 'p3', 8), 8]),
     (4.11,
      [1,
       (1, 'p1', 2),
       2,
       (2, 'p4', 3),
       3,
       (3, 'p6', 4),
       4,
       (4, 'p1', 9),
       9,
       (9, 'p2', 8),
       8]),
     (4.21,
      [1,
       (1, 'p2', 2),
       2,
       (2, 'p4', 3),
       3,
       (3, 'p6', 4),
       4,
       (4, 'p1', 9),
       9,
       (9, 'p2', 8),
       8]),
     (4.3100000000000005,
      [1,
       (1, 'p3', 2),
       2,
       (2, 'p4', 3),
       3,
       (3, 'p6', 4),
       4,
       (4, 'p1', 9),
       9,
       (9, 'p2', 8),
       8]),
     (4.321000000000001,
      [1,
       (1, 'p1', 2),
       2,
       (2, 'p5', 3),
       3,
       (3, 'p6', 4),
       4,
       (4, 'p1', 9),
       9,
       (9, 'p2', 8),
       8]),
     (4.421,
      [1,
       (1, 'p2', 2),
       2,
       (2, 'p5', 3),
       3,
       (3, 'p6', 4),
       4,
       (4, 'p1', 9),
       9,
       (9, 'p2', 8),
       8]),
     (4.521,
      [1,
       (1, 'p3', 2),
       2,
       (2, 'p5', 3),
       3,
       (3, 'p6', 4),
       4,
       (4, 'p1', 9),
       9,
       (9, 'p2', 8),
       8])]

    """
    def remove_node(node):
        """
        Removes node from Graph, by removing all of it's edges.
        The removed edges are appended to the removed_edges set.

        Format of edge: (source,predicate,sink)

        :param node: The node to be removed.
        """
        for u,v,key,atrr_dict in Graph.out_edges_iter(node, data=True,keys=True):
            removed_edges.add((u,key,v))

        for u,v,key,atrr_dict in Graph.in_edges_iter(node, data=True,keys=True):
            removed_edges.add((u,key,v))

    # Determine the shortest path from the source to the sink.
    l0,p0 = single_source_dijkstra_2(Graph,source,sink,blacklist,weight=weight)

    if sink not in l0:
        raise nx.NetworkXNoPath("node %s not reachable from %s" % (source, sink))

    A = [p0[sink]]
    A_costs = [l0[sink]]

    # First solution
    yield (A_costs[0],A[0])

    # Initialize the heap to store the potential kth shortest path.
    B = []

    k=0

    while True:
        k+=1

        # The spur node ranges from the first node to the next to last node in the shortest path.
        for i in range(0,len(A[-1])-2,2): # skip edges by using step = 2

            # Spur node is retrieved from the previous k-shortest path, k − 1.
            # i is even thus it is always a node
            spurNode = A[-1][i]

            # The path from the source to the spur node of the previous k-shortest path.
            rootPath = A[-1][:i+1]    # CAUTION! This is an odd length range, so appropriate for paths. This is done so that for i=0, the first node is returned. If we used i, an epty list would be returned.

            # We store the removed edges: item = (source,predicate,sink)
            removed_edges = set()

            for path in A:
                if rootPath == path[:i+1]:
                    u,p,v=path[i+1] # always an edge since paths have odd length.
                    if Graph.has_edge(u, v, p) and (u, p, v) not in blacklist:
                        # Remove the links that are part of the previous shortest paths which share the same root path.
                        removed_edges.add((u,p,v))

            # for each node rootPathNode in rootPath except spurNode (the last node)
            for n in range(0,len(rootPath)-2,2): #spurNode is always the last node in the rootPath!
                rootPathNode = rootPath[n]  # By setting step=2 we are reading only nodes.
                remove_node(rootPathNode)

            # Calculate the spur path from the spur node to the sink.
            spurPathlength,spurPath = single_source_dijkstra_2(Graph, spurNode, sink,blacklist | removed_edges,weight=weight)

            if sink in spurPath and spurPath[sink]:
                # Entire path is made up of the root path and spur path.
                totalPath = rootPath[:-1] + spurPath[sink] # last item of rootPath equals first item of spurPath, so we remove it to respect path continuity after the merging.
                totalPathlength = get_path_length(inGraph,rootPath)+spurPathlength[sink]
                heappush(B, (totalPathlength, totalPath))

            # clear list of removed edges
            removed_edges = set()

        if B:
            cost_, path_ = heappop(B)
            A.append(path_)
            A_costs.append(cost_)
            yield (cost_,path_)
        else:
            break
    return
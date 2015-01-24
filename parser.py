"""
Minor changes to the original edge-list parsing functions of Networkx. 
When used with a nx.MultiDiGraph() each edge in the edge-list is added to 
the graph with a specific key. The key corresponds to the 'label' value 
of each line in the edge-list.

:author: Spyridon Kazanas
:contact: s.kazanas@gmail.com
"""
import networkx as nx
from networkx.utils.decorators import open_file

def parse_edgelist_2(lines, comments='#', delimiter=None,
                   create_using=None, nodetype=None, data=True):
    """Parse lines of an edge list representation of a graph.
    """
    from ast import literal_eval
    if create_using is None:
        G=nx.Graph()
    else:
        try:
            G=create_using
            G.clear()
        except:
            raise TypeError("create_using input is not a NetworkX graph type")

    for line in lines:
        p=line.find(comments)
        if p>=0:
            line = line[:p]
        if not len(line):
            continue
        # split line, should have 2 or more
        s=line.strip().split(delimiter)
        if len(s)<2:
            continue
        u=s.pop(0)
        v=s.pop(0)
        d=s
        if nodetype is not None:
            try:
                u=nodetype(u)
                v=nodetype(v)
            except:
                raise TypeError("Failed to convert nodes %s,%s to type %s."
                                %(u,v,nodetype))

        if len(d)==0 or data is False:
            # no data or data type specified
            edgedata={}
        elif data is True:
            # no edge types specified
            try: # try to evaluate as dictionary
                edgedata=dict(literal_eval(' '.join(d)))
            except:
                raise TypeError(
                    "Failed to convert edge data (%s) to dictionary."%(d))
        else:
            # convert edge data to dictionary with specified keys and type
            if len(d)!=len(data):
                raise IndexError(
                    "Edge data %s and data_keys %s are not the same length"%
                    (d, data))
            edgedata={}
            for (edge_key,edge_type),edge_value in zip(data,d):
                try:
                    edge_value=edge_type(edge_value)
                except:
                    raise TypeError(
                        "Failed to convert %s data %s to type %s."
                        %(edge_key, edge_value, edge_type))
                edgedata.update({edge_key:edge_value})
        G.add_edge(u, v,edgedata['label'], attr_dict=edgedata)
    return G

@open_file(0,mode='rb')
def read_edgelist_2(path, comments="#", delimiter=None, create_using=None, 
                  nodetype=None, data=True, edgetype=None, encoding='utf-8'):
    """Read a graph from a list of edges.

    Parameters
    ----------
    path : file or string
       File or filename to write. If a file is provided, it must be
       opened in 'rb' mode.
       Filenames ending in .gz or .bz2 will be uncompressed.
    comments : string, optional
       The character used to indicate the start of a comment. 
    delimiter : string, optional
       The string used to separate values.  The default is whitespace.
    create_using : Graph container, optional, 
       Use specified container to build graph.  The default is networkx.Graph,
       an undirected graph.
    nodetype : int, float, str, Python type, optional
       Convert node data from strings to specified type
    data : bool or list of (label,type) tuples
       Tuples specifying dictionary key names and types for edge data
    edgetype : int, float, str, Python type, optional OBSOLETE
       Convert edge data from strings to specified type and use as 'weight'
    encoding: string, optional
       Specify which encoding to use when reading file.

    Returns
    -------
    G : graph
       A networkx Graph or other type specified with create_using

    Examples
    --------
    >>> nx.write_edgelist(nx.path_graph(4), "test.edgelist")
    >>> G=nx.read_edgelist("test.edgelist")

    >>> fh=open("test.edgelist", 'rb')
    >>> G=nx.read_edgelist(fh)
    >>> fh.close()

    >>> G=nx.read_edgelist("test.edgelist", nodetype=int)
    >>> G=nx.read_edgelist("test.edgelist",create_using=nx.DiGraph())

    Edgelist with data in a list:

    >>> textline = '1 2 3'
    >>> fh = open('test.edgelist','w')
    >>> d = fh.write(textline)
    >>> fh.close()
    >>> G = nx.read_edgelist('test.edgelist', nodetype=int, data=(('weight',float),))
    >>> G.nodes()
    [1, 2]
    >>> G.edges(data = True)
    [(1, 2, {'weight': 3.0})]

    See parse_edgelist() for more examples of formatting.

    See Also
    --------
    parse_edgelist

    Notes
    -----
    Since nodes must be hashable, the function nodetype must return hashable
    types (e.g. int, float, str, frozenset - or tuples of those, etc.) 
    """
    lines = (line.decode(encoding) for line in path)
    return parse_edgelist_2(lines,comments=comments, delimiter=delimiter,
                          create_using=create_using, nodetype=nodetype,
                          data=data)
'''
SELECT DISTINCT * {
?a a <http://www.w3.org/2002/07/owl#Thing>.
?a a <http://dbpedia.org/class/yago/Anatomy106057539>.
?a a <http://dbpedia.org/ontology/AnatomicalStructure>.
?a ((!a)*/<http://dbpedia.org/ontology/drainsTo>)|(<http://dbpedia.org/ontology/drainsTo>/(!a)*) ?b.
?b a <http://www.w3.org/2002/07/owl#Thing>.
?b a <http://dbpedia.org/ontology/Vein>.
?b a <http://dbpedia.org/ontology/AnatomicalStructure>.
} LIMIT 100
'''

from RDFTypeSummary import *
import networkx as nx
from corefunctions import *

mysum=RDFTypeSummary("/home/spyros/Documents/Paper-Evaluation-2/RDF-Type-Summary-graphs-new/benchmark_1.summary")

q_s=frozenset(["http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/class/yago/Anatomy106057539","http://dbpedia.org/ontology/AnatomicalStructure"])
q_t=frozenset(["http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/ontology/Vein","http://dbpedia.org/ontology/AnatomicalStructure"])
q_p="http://dbpedia.org/ontology/drainsTo"
q_l=2

tu1=frozenset(['http://www.w3.org/2002/07/owl#Thing','http://dbpedia.org/class/yago/Vein105418717','http://dbpedia.org/ontology/Vein','http://dbpedia.org/ontology/AnatomicalStructure'])
tu2=frozenset(['http://www.w3.org/2002/07/owl#Thing','http://dbpedia.org/ontology/Vein','http://dbpedia.org/ontology/AnatomicalStructure'])
p1_1='http://dbpedia.org/ontology/vein'
p1_2='http://dbpedia.org/property/vein'
p2_1='http://dbpedia.org/ontology/drainsTo'
p2_2='http://dbpedia.org/property/drainsto'
lostpath_1=[q_s,(q_s,p1_1,tu1),tu1,(tu1,p2_1,tu2),tu2,(tu2,q_p,q_t),q_t]
lostpath_2=[q_s,(q_s,p1_2,tu1),tu1,(tu1,p2_1,tu2),tu2,(tu2,q_p,q_t),q_t]
lostpath_3=[q_s,(q_s,p1_1,tu1),tu1,(tu1,p2_2,tu2),tu2,(tu2,q_p,q_t),q_t]
lostpath_4=[q_s,(q_s,p1_2,tu1),tu1,(tu1,p2_2,tu2),tu2,(tu2,q_p,q_t),q_t]

#mysum.execute_query_3(q_s,q_p,q_t,q_l)
g=mysum.db_graph

pg=YenKSP_generator(g,q_s,q_t,set())
all_simple_paths = [p for p in nx.all_simple_paths(g, q_s, target=q_t, cutoff=3)]
i=0
for e in g.edges():
    if e[0]==e[1]:
        i+=1
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
mysum=RDFTypeSummary("/home/spyros/Documents/Paper-Evaluation-2/RDF-Type-Summary-graphs-new/benchmark_1.summary")

q_s=frozenset(["http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/class/yago/Anatomy106057539","http://dbpedia.org/ontology/AnatomicalStructure"])
q_t=frozenset(["http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/ontology/Vein","http://dbpedia.org/ontology/AnatomicalStructure"])
q_p="http://dbpedia.org/ontology/drainsTo"
q_l=2

mysum.execute_query(q_s,q_p,q_t,q_l)
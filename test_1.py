from RDFTypeSummary import *

mysum=RDFTypeSummary("/home/spyros/Documents/Paper-Evaluation-2/RDF-Type-Summary-graphs-new/benchmark_10.summary")

q_s=frozenset(["http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/ontology/Award"])
q_t=frozenset(["http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/ontology/MusicGenre"])
q_p="http://dbpedia.org/ontology/genre"
q_l=10

mysum.execute_query(q_s,q_p,q_t,q_l)

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

mysum=RDFTypeSummary("/home/spyros/Documents/Paper-Evaluation-2/RDF-Type-Summary-graphs-new/benchmark_1.summary")

q_s=frozenset(["http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/class/yago/Anatomy106057539","http://dbpedia.org/ontology/AnatomicalStructure"])
q_t=frozenset(["http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/ontology/Vein","http://dbpedia.org/ontology/AnatomicalStructure"])
q_p="http://dbpedia.org/ontology/drainsTo"
q_l=2

mysum.execute_query(q_s,q_p,q_t,q_l)

g_source_removed=set([(e[0],e[2],e[1]) for e in mysum.db_graph.out_edges_iter([q_source],data=False, keys=True) if e[2] != q_predicate])
g_target_removed=set([(e[0],e[2],e[1]) for e in mysum.db_graph.in_edges_iter([q_target],data=False, keys=True) if e[2] == q_predicate])


pathgen1 = YenKSP_generator(mysum.db_graph,q_source,q_target,g_source_removed)
pathgen2 = YenKSP_generator(mysum.db_graph,q_source,q_target,g_target_removed)


edges=[(1, 2, 'p2', {'weight': 0.2, 'label':'p2'}),
(1, 2, 'p3', {'weight': 0.3, 'label':'p3'}),
(1, 2, 'p1', {'weight': 0.1, 'label':'p1'}),
(2, 1, 'p3', {'weight': 0.21, 'label':'p3'}),
(2, 3, 'p4', {'weight': 0.21, 'label':'p4'}),
(2, 3, 'p5', {'weight': 0.421, 'label':'p5'}),
(3, 4, 'p6', {'weight': 0.6, 'label':'p6'}),
(4, 9, 'p1', {'weight': 1.6, 'label':'p1'}),
(9, 8, 'p2', {'weight': 1.6, 'label':'p2'}),
(3, 5, 'p7', {'weight': 0.3, 'label':'p7'}),
(3, 6, 'p7', {'weight': 0.1, 'label':'p7'}),
(5, 8, 'p3', {'weight': 0.4, 'label':'p3'}),
(6, 1, 'p1', {'weight': 0.1, 'label':'p1'})]

G=nx.MultiDiGraph()
for e in edges:
    G.add_edge(e[0],e[1],e[2],e[3])
    
    
'''
SELECT DISTINCT ?_a ?_b {
{SELECT DISTINCT * WHERE { 
?_a a <http://www.w3.org/2002/07/owl#Thing> . 
?_a a <http://dbpedia.org/class/yago/Anatomy106057539> . 
?_a a <http://dbpedia.org/ontology/AnatomicalStructure> . 
?_b a <http://www.w3.org/2002/07/owl#Thing> . 
?_b a <http://dbpedia.org/ontology/Vein> . 
?_b a <http://dbpedia.org/ontology/AnatomicalStructure> . 
?_a !a ?_1_2 . 
?_1_2 <http://dbpedia.org/ontology/drainsTo> ?_b . }
}UNION{
SELECT DISTINCT * WHERE {
?_a a <http://www.w3.org/2002/07/owl#Thing> . 
?_a a <http://dbpedia.org/class/yago/Anatomy106057539> . 
?_a a <http://dbpedia.org/ontology/AnatomicalStructure> . 
?_b a <http://www.w3.org/2002/07/owl#Thing> . 
?_b a <http://dbpedia.org/ontology/Vein> . 
?_b a <http://dbpedia.org/ontology/AnatomicalStructure> . 
?_a !a ?_2_2 .
?_2_2 !a ?_2_3 .
?_2_3 <http://dbpedia.org/ontology/drainsTo> ?_b . }
}UNION{
SELECT DISTINCT * WHERE {
?_a a <http://www.w3.org/2002/07/owl#Thing> . 
?_a a <http://dbpedia.org/class/yago/Anatomy106057539> . 
?_a a <http://dbpedia.org/ontology/AnatomicalStructure> . 
?_b a <http://www.w3.org/2002/07/owl#Thing> . 
?_b a <http://dbpedia.org/ontology/Vein> . 
?_b a <http://dbpedia.org/ontology/AnatomicalStructure> . 
?_a !a ?_3_2 .
?_3_2 !a ?_3_3 .
?_3_3 !a ?_3_4 .
?_3_4 <http://dbpedia.org/ontology/drainsTo> ?_b . }
}}LIMIT 1000

'''

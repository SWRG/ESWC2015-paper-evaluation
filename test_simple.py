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

from RDFTypeSummary import *

mysum=RDFTypeSummary()

q_s=frozenset(["http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/class/yago/Anatomy106057539","http://dbpedia.org/ontology/AnatomicalStructure"])
q_t=frozenset(["http://www.w3.org/2002/07/owl#Thing","http://dbpedia.org/ontology/Vein","http://dbpedia.org/ontology/AnatomicalStructure"])
q_p="http://dbpedia.org/ontology/drainsTo"
q_l=2

'''
TODO: Duplicate results elimination!
TODO: Support case where edge is the first edge of the path!
'''
mysum.execute_query2(q_s,q_p,q_t,q_l)

import sys,os
sys.path.insert(0,os.path.abspath(__file__+"/../.."))
import yenalgo2,corefunctions
import networkx as nx
import unittest

class KnownValues(unittest.TestCase):
    g = nx.Graph()
    g.add_edge(1,2,{'weight':1})
    g.add_edge(1,3,{'weight':2})
    g.add_edge(1,4,{'weight':3})
    g.add_edge(2,5,{'weight':2})
    g.add_edge(2,6,{'weight':1})
    g.add_edge(3,7,{'weight':1})
    g.add_edge(3,8,{'weight':3})
    g.add_edge(3,9,{'weight':4})
    g.add_edge(3,10,{'weight':1})
    g.add_edge(4,10,{'weight':2})
    g.add_edge(4,11,{'weight':2})
    g.add_edge(5,12,{'weight':1})
    g.add_edge(6,13,{'weight':2})
    g.add_edge(10,14,{'weight':2})
    g.add_edge(14,15,{'weight':2})
    (s,t)=(3,15)

    knownValuesYen = (
    ((1,2),[(1.0, [1, 2])]),
    ((3,15),[(5.0, [3, 10, 14, 15]), (11.0, [3, 1, 4, 10, 14, 15])]),
    ((1,15),[(7.0, [1, 3, 10, 14, 15]), (9.0, [1, 4, 10, 14, 15])]),
    ((4,15),[(6.0, [4, 10, 14, 15]), (10.0, [4, 1, 3, 10, 14, 15])])
    )

    def test_YenKSP_generator_KnownValues(self):
        """YenKSP_generator should give known result with known input"""
        for ((source,target), expected_result) in self.knownValuesYen:
            result = [p for p in corefunctions.YenKSP_generator(self.g,source,target)]
            self.assertEqual(expected_result, result)

    def test_yenalgo2_KnownValues(self):
        """yenalgo2 should give known result with known input"""
        for ((source,target), expected_result) in self.knownValuesYen:
            result = [p for p in yenalgo2.k_shortest_paths(self.g,source,target,4)]
            self.assertEqual(expected_result, result)

if __name__ == "__main__":
    unittest.main()

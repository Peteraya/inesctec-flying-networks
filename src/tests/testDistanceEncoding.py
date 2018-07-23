import context
import unittest
import utils
import math

class testDistanceEncoding(unittest.TestCase):
    def test_sparse_to_distance_simple(self):
        matrix = [[1, 0], [0, 0]]
        new_matrix = utils.sparse_to_distance(matrix)
        self.assertSequenceEqual(new_matrix.tolist(), [[0, 1], [1, math.sqrt(2)]])
    
    def test_sparse_to_distances_multiple_1s(self):
        matrix = [[0, 1, 0], [0, 0, 0], [0, 0, 1], [1, 0, 0]]
        new_matrix = utils.sparse_to_distance(matrix)
        self.assertSequenceEqual(new_matrix.tolist(), [[1, 0, 1], [math.sqrt(2), 1, 1], [1, 1, 0], [0, 1, 1]])

if(__name__ == '__main__'):
    unittest.main()
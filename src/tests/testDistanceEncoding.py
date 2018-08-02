"""
This module implements the class testDistanceEncoding,
which implements the unit tests related to the conversion of a matrix to distance encoding form.
"""
import context
import unittest
import math
import utils



class testDistanceEncoding(unittest.TestCase):
    """
    Implements unit tests related to the conversion of a matrix to distance encoding form.
    """
    def test_sparse_distance_simple(self):
        """
        Tests a simple conversion from sparse to distance encoding.
        """
        matrix = [[1, 0], [0, 0]]
        new_matrix = utils.sparse_to_distance(matrix)
        self.assertSequenceEqual(new_matrix.tolist(), [[0, 1], [1, math.sqrt(2)]])

    def test_sparse_distance_multiple1s(self):
        """
        Tests a complex conversion from sparse to distance encoding, where the sparse matrix has multiple 1's.
        """
        matrix = [[0, 1, 0], [0, 0, 0], [0, 0, 1], [1, 0, 0]]
        new_matrix = utils.sparse_to_distance(matrix)
        self.assertSequenceEqual(new_matrix.tolist(), [[1, 0, 1], [math.sqrt(2), 1, 1], [1, 1, 0], [0, 1, 1]])

if __name__ == '__main__':
    unittest.main()

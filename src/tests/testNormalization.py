"""
This module implements the class testNormalization, 
which implements the unit tests related to the normalization of matrices.
"""
import context
import unittest
import numpy
from sklearn import preprocessing
import utils



class TestNormalization(unittest.TestCase):
    """
    This class implements the unit tests related to the normalization of matrices.
    """
    def test_stats_matrix(self):
        """
        Implements unit tests related to the retrieval of mean and standard deviation from a matrix.
        """
        matrix = numpy.random.rand(3, 4)
        matrix_array = numpy.ravel(matrix)
        mean = numpy.mean(matrix_array)
        std = numpy.std(matrix_array)
        stats_mean, stats_std = utils.stats_matrix(matrix)
        self.assertAlmostEqual(stats_mean, mean)
        self.assertAlmostEqual(stats_std, std)

    def test_normalize_matrix_standard(self):
        """
        Implements unit tests related to the normalization of a matrix to the standard form.
        """
        matrix = numpy.array([[1.0, 2.0, 3.0, 4.0], [3.0, 4.0, 5.0, 6.0], [5.0, 6.0, 7.0, 8.0]])
        matrix_array = numpy.ravel(matrix)
        normalized_matrix_array = preprocessing.scale(matrix_array)
        normalized_matrix = normalized_matrix_array.reshape(3,4)
        new_matrix = utils.normalize_matrix(matrix, 0, 1)
        self.assertSequenceEqual(new_matrix.tolist(), normalized_matrix.tolist())

    def test_normalize_matrix_generic(self):
        """
        Implements unit tests related to the normalization of a matrix
        given a certain mean and standard of deviation.
        """
        matrix = numpy.array([[1.0, 2.0, 3.0, 4.0], [3.0, 4.0, 5.0, 6.0], [5.0, 6.0, 7.0, 8.0]])
        new_matrix = utils.normalize_matrix(matrix, 2, 4)
        new_mean = numpy.mean(numpy.ravel(new_matrix))
        new_std = numpy.std(numpy.ravel(new_matrix))
        self.assertAlmostEqual(new_mean, 2)
        self.assertAlmostEqual(new_std, 4)

if __name__ == '__main__':
    unittest.main()
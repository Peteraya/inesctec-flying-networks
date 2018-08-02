"""
This module implements the class testTransformations,
which implements the unit tests related to the transformation of a matrix.
"""
import context
import unittest
import utils


class TestTransformations(unittest.TestCase):
    """
    This class imlements the unit tests related to the transformation of a matrix.
    """
    def test_rotation_90(self):
        """
        Tests rotation of a matrix by 90º.
        """
        matrix = [[1, 2], [3, 4]]
        #The matrix is:
        #3 4
        #1 2
        new_matrix = utils.transform_matrix(matrix, utils.rotate, 90)
        #New matrix should be:
        #1 3
        #2 4
        self.assertSequenceEqual(new_matrix.tolist(), [[2, 4], [1, 3]])

    def test_rotation_180(self):
        """
        Tests rotation of a matrix by 180º.
        """
        matrix = [[1, 2], [3, 4]]
        #The matrix is:
        #3 4
        #1 2
        new_matrix = utils.transform_matrix(matrix, utils.rotate, 180)
        #New matrix should be:
        #2 1
        #4 3
        self.assertSequenceEqual(new_matrix.tolist(), [[4, 3], [2, 1]])

    def test_rotation_270(self):
        """
        Tests rotation of a matrix by 270º.
        """
        matrix = [[1, 2], [3, 4]]
        # The matrix is:
        # 3 4
        # 1 2
        new_matrix = utils.transform_matrix(matrix, utils.rotate, 270)
        # New matrix should be:
        # 4 2
        # 3 1
        self.assertSequenceEqual(new_matrix.tolist(), [[3, 1], [4, 2]])

    def test_symmetry_0(self):
        """
        Tests symmetry of a matrix with axis at 0º.
        """
        matrix = [[1, 2], [3, 4]]
        # The matrix is:
        # 3 4
        # 1 2
        new_matrix = utils.transform_matrix(matrix, utils.symmetric, 0)
        # New matrix should be:
        # 1 2
        # 3 4
        self.assertSequenceEqual(new_matrix.tolist(), [[3, 4], [1, 2]])

    def test_symmetry_45(self):
        """
        Tests symmetry of a matrix with axis at 45º.
        """
        matrix = [[1, 2], [3, 4]]
        # The matrix is:
        # 3 4
        # 1 2
        new_matrix = utils.transform_matrix(matrix, utils.symmetric, 45)
        # New matrix should be:
        # 2 4
        # 1 3
        self.assertSequenceEqual(new_matrix.tolist(), [[1, 3], [2, 4]])

    def test_symmetry_90(self):
        """
        Tests symmetry of a matrix with axis at 90º.
        """
        matrix = [[1, 2], [3, 4]]
        # The matrix is:
        # 3 4
        # 1 2
        new_matrix = utils.transform_matrix(matrix, utils.symmetric, 90)
        # New matrix should be:
        # 4 3
        # 2 1
        self.assertSequenceEqual(new_matrix.tolist(), [[2, 1], [4, 3]])

    def test_symmetry_135(self):
        """
        Tests symmetry of a matrix with axis at 135º.
        """
        matrix = [[1, 2], [3, 4]]
        # The matrix is:
        # 3 4
        # 1 2
        new_matrix = utils.transform_matrix(matrix, utils.symmetric, 135)
        # New matrix should be:
        # 3 1
        # 4 2
        self.assertSequenceEqual(new_matrix.tolist(), [[4, 2], [3, 1]])

    def test_large_matrix_rotate_270(self):
        """
        Tests rotation of a large matrix by 270º.
        """
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # The matrix is:
        # 7 8 9
        # 4 5 6
        # 1 2 3
        new_matrix = utils.transform_matrix(matrix, utils.rotate, 270)
        # New matrix is:
        # 9 6 3
        # 8 5 2
        # 7 4 1
        self.assertSequenceEqual(new_matrix.tolist(), [[7, 4, 1], [8, 5, 2], [9, 6, 3]])

    def test_large_matrix_symmetry_45(self):
        """
        Tests the symmetry of a large matrix with axis at 45º.
        """
        matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        # The matrix is:
        # 7 8 9
        # 4 5 6
        # 1 2 3
        new_matrix = utils.transform_matrix(matrix, utils.symmetric, 45)
        # New matrix is:
        # 3 6 9
        # 2 5 8
        # 1 4 7
        self.assertSequenceEqual(new_matrix.tolist(), [[1, 4, 7], [2, 5, 8], [3, 6, 9]])

if __name__ == '__main__':
    unittest.main()
    
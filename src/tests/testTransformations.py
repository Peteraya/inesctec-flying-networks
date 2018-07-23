import context
import unittest
import utils

class TestTransformations(unittest.TestCase):
    def test_rotation_90(self):
        matrix = [[1,2], [3,4]] 
        #The matrix is:
        #3 4
        #1 2
        new_matrix = utils.transform_matrix(matrix,utils.rotate, 90)
        #New matrix should be:
        #1 3
        #2 4
        self.assertSequenceEqual(new_matrix.tolist(), [[2, 4], [1, 3]])

    def test_rotation_180(self):
        matrix = [[1,2], [3,4]] 
        #The matrix is:
        #3 4
        #1 2
        new_matrix = utils.transform_matrix(matrix,utils.rotate, 180)
        #New matrix should be:
        #2 1
        #4 3
        self.assertSequenceEqual(new_matrix.tolist(), [[4, 3], [2, 1]])

    def test_rotation_270(self):
        matrix = [[1,2], [3,4]] 
        # The matrix is:
        # 3 4
        # 1 2
        new_matrix = utils.transform_matrix(matrix,utils.rotate, 270)
        # New matrix should be:
        # 4 2
        # 3 1
        self.assertSequenceEqual(new_matrix.tolist(), [[3, 1], [4, 2]])
    
    def test_symmetry_0(self):
        matrix = [[1,2], [3,4]] 
        # The matrix is:
        # 3 4
        # 1 2
        new_matrix = utils.transform_matrix(matrix,utils.symmetric, 0)
        # New matrix should be:
        # 1 2
        # 3 4
        self.assertSequenceEqual(new_matrix.tolist(), [[3, 4], [1, 2]])

    def test_symmetry_45(self):
        matrix = [[1,2], [3,4]] 
        # The matrix is:
        # 3 4
        # 1 2
        new_matrix = utils.transform_matrix(matrix,utils.symmetric, 45)
        # New matrix should be:
        # 2 4
        # 1 3
        self.assertSequenceEqual(new_matrix.tolist(), [[1, 3], [2, 4]])

    def test_symmetry_90(self):
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
        matrix = [[1, 2], [3, 4]]
        # The matrix is:
        # 3 4
        # 1 2
        new_matrix = utils.transform_matrix(matrix, utils.symmetric, 135)
        # New matrix should be:
        # 3 1
        # 4 2
        self.assertSequenceEqual(new_matrix.tolist(), [[4, 2], [3, 1]])


if(__name__== '__main__'):
    unittest.main()
    
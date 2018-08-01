"""
This module contains generic functions that are used by other modules in the program
"""
import random
import math
import numpy as np



def rotate(size, coordinate_x, coordinate_y, angle):
    """
    Function that given a set of coordinates of a cell square matrix, returns the new coordinates of that cell after a rotation has been applied.  
    
    Args:
        size: size of the matrix
        coordinate_x: X coordinate of the cell
        coordinate_y: Y coordinate of the cell
        angle: Angle of the rotation. Must be in [90, 180, 270]
    
    Returns:
        New coordinates of the cell to which a rotation has been applied

    Raises:
        ValueError: If angle doesn't belong to [90, 180, 270]
    """
    if angle == 90:
        return coordinate_y, size - 1 - coordinate_x
    elif angle == 180:
        return size - 1 - coordinate_x, size - 1 - coordinate_y
    elif angle == 270:
        return size - 1 - coordinate_y, coordinate_x
    else:
        raise ValueError('The angle of a rotation can only be one of [90, 180, 270]')


def symmetric(size, coordinate_x, coordinate_y, angle_axis):
    """
    Function that given a set of coordinates of a cell square matrix, returns the new coordinates of that cell after a symmetry has been applied.  
    
    Args:
        size: size of the matrix
        coordinate_x: X coordinate of the cell
        coordinate_y: Y coordinate of the cell
        angle: Angle of the rotation. Must be in [0, 45, 90, 135]
    
    Returns:
        New coordinates of the cell to which a symmetry has been applied

    Raises:
        ValueError: If angle doesn't belong to [0, 45, 90, 135]
    """
    if angle_axis == 0:
        return coordinate_x, size - 1 - coordinate_y
    elif angle_axis == 45:
        return coordinate_y, coordinate_x
    elif angle_axis == 90:
        return size - 1 - coordinate_x, coordinate_y
    elif angle_axis == 135:
        return size - 1 - coordinate_y, size - 1 - coordinate_x
    else:
        raise ValueError('The angle of a symmetry can only be one of [0, 45, 90, 135]')


def transform_matrix(matrix, function, angle):
    """
    Function that applies a transformation (rotation or symmetry) to a matrix  
    
    Args:
        matrix: Matrix to be transformed
        function: Function that defines the transformation to apply (rotate or symmetry)
        angle: Angle of the transformation
    
    Returns:
        New matrix to which the original matrix was transformed to

    Raises:
        ValueError: If matrix is empty (i.e. has size 0)
        ValueError: If matrix is not square
    """
    if len(matrix) == 0:
        raise ValueError('The matrix must have size bigger than 0')
    elif not(len(matrix) == len(matrix[0])):
        raise ValueError('The matrix must be square')

    size = len(matrix)
    new_matrix = np.empty((size, size), dtype = 'float')
    for coordinate_y in range(len(matrix)):
        for coordinate_x in range(len(matrix[coordinate_y])):
            new_x, new_y = function(size, coordinate_x, coordinate_y, angle)
            new_matrix[new_y][new_x] = matrix[coordinate_y][coordinate_x]
    return new_matrix    

def distance(cell1, cell2):
    """
    Function that computes the euclidian distance between two pairs of coordinates

    Args:
        cell1: First cell of the pair of cells whose distance will be computed. Consists of a list with two float elements.
        cell2: Second cell of the pair of cells whose distance will be computed. Consists of a list with two float elements.
    
    Returns:
        Euclidian distance between the two cells
    """
    return math.sqrt((cell1[0]-cell2[0])*(cell1[0]-cell2[0]) + (cell1[1]-cell2[1])*(cell1[1]-cell2[1]) )

def sparse_to_distance(sparse_matrix):
    drone_positions = []
    for i in range(len(sparse_matrix)):
        for j in range(len(sparse_matrix[i])):
            if(sparse_matrix[i][j] == 1):
                drone_positions.append([i, j])
    
    distance_matrix=np.empty((len(sparse_matrix), len(sparse_matrix[0])), dtype='float')
    for i in range(len(distance_matrix)):
        for j in range(len(distance_matrix[i])):
            min_distance = len(distance_matrix) + len(distance_matrix[i]) + 1
            for k in range(len(drone_positions)):
                new_distance = distance([i, j], drone_positions[k])
                if(new_distance < min_distance):
                    min_distance = new_distance
            distance_matrix[i][j] = min_distance 

    return distance_matrix

def stats_matrix(matrix):
    sum = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            sum += matrix[i][j]
    
    matrix_noElems = len(matrix) * len(matrix[0])
    mean = sum / matrix_noElems
    sum_std = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            sum_std += (matrix[i][j] - mean)*(matrix[i][j] - mean)
  
    std = math.sqrt(sum_std / matrix_noElems)

    return mean, std

def normalize_matrix(matrix, new_mean, new_std):
    new_matrix = np.empty((len(matrix), len(matrix[0])), dtype='float')
    mean, std = stats_matrix(matrix)
    for i in range(len(matrix)):
       for j in range(len(matrix[0])):
           new_matrix[i][j] = ((matrix[i][j] - mean) / std) * new_std + new_mean
    return new_matrix


def matrix_multiply_add(matrix, new_mean, new_std):
    new_matrix = np.empty((len(matrix), len(matrix[0])), dtype='float')
    for i in range(len(matrix)):
       for j in range(len(matrix[0])):
           new_matrix[i][j] = matrix[i][j] * new_std + new_mean
    return new_matrix

def round_matrix(matrix, decimal_points):
    new_matrix = np.empty((len(matrix), len(matrix[0])), dtype='float')
    for i in range(len(matrix)):
       for j in range(len(matrix[0])):
           new_matrix[i][j] = round(matrix[i][j], decimal_points)
    return new_matrix

def shuffle_input_data(input_x, input_y):
    struct_to_shuffle = []
    for i in range(len(input_x)):
        struct_to_shuffle.append([input_x[i], input_y[i]])
    random.shuffle(struct_to_shuffle)
    new_input_x = []
    new_input_y = []
    for element in struct_to_shuffle:
        new_input_x.append(element[0])
        new_input_y.append(element[1])
    return np.array(new_input_x), np.array(new_input_y)

import numpy as np
import pandas as pd
import math
import os, glob
import codecs, json
import random

def rotate(size, x, y, angle):
    if angle == 90:
        return y, size - 1 - x
    elif angle == 180:
        return size - 1 - x, size - 1 - y
    elif angle == 270:
        return size - 1 - y, x


def symmetric(size, x, y, angle_axis):
    if angle_axis == 0:
        return x, size - 1 - y
    elif angle_axis == 45:
        return y, x
    elif angle_axis == 90:
        return size - 1 - x, y
    elif angle_axis == 135:
        return size - 1 - y, size - 1 - x 

#Note: the matrix has to be square
def transform_matrix(matrix, function, angle):
    size = len(matrix)
    new_matrix = np.empty((size, size), dtype = 'float')
    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            new_x, new_y = function(size, x, y, angle)
            new_matrix[new_y][new_x] = matrix[y][x]
    return new_matrix    

def distance(cell1, cell2):
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



    




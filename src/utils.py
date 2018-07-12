import numpy as np
import pandas as pd
import math

def rotate(size, x, y, angle):
    if angle == 90:
        return y, size - 1 - x
    elif angle == 180:
        return size - 1 - x, size - 1 - y
    elif angle == 270:
        return size - 1 - y, x


def simmetric(size, x, y, angle_axis):
    if angle_axis == 0:
        return x, size - 1 - y
    elif angle_axis == 45:
        return y, x
    elif angle_axis == 90:
        return size - 1 - x, y
    elif angle_axis == 135:
        return size - 1 - y, size - 1 - x 

#transform_scenarios(scenarios, 10, rotate, 90)  #possible angles: 90, 180, 270
#transform_scenarios(scenarios, 10, simmetric, 0)  #possible angles: 0, 45, 90, 135
def transform_scenarios(scenarios, size, function, angle):
    new_scenarios = pd.DataFrame(columns = ['x', 'y', 'dataRateMbps'])
    for y in range(0, size):
        for x in range(0, size):
            i = y * size + x
            new_scenarios.loc[i, 'x'] = x
            new_scenarios.loc[i, 'y'] = y

    for y in range(0, size):
        for x in range(0, size):
            i = y * size + x
            new_x, new_y = function(size, scenarios.loc[i, 'x'], scenarios.loc[i, 'y'], angle)
            new_scenarios.loc[new_y*size + new_x, 'dataRateMbps'] = scenarios.loc[i, 'dataRateMbps']
    return new_scenarios

#transform_results(results, 10, rotate, 90) #possible angles: 90, 180, 270
#transform_results(results, 10, simmetric, 45) #possible angles: 0, 45, 90, 135
def transform_results(results, size, function, angle):
    new_results = results.copy() 
    for i in range(len(results)):
        new_x, new_y = function(size, results.loc[i, 'fmap1CoordinatesX'], results.loc[i, 'fmap1CoordinatesY'], angle)
        new_results.loc[i, 'fmap1CoordinatesX'] = new_x
        new_results.loc[i, 'fmap1CoordinatesY'] = new_y
        new_x, new_y = function(size, results.loc[i, 'fmap2CoordinatesX'], results.loc[i, 'fmap2CoordinatesY'], angle)
        new_results.loc[i, 'fmap2CoordinatesX'] = new_x
        new_results.loc[i, 'fmap2CoordinatesY'] = new_y
        new_x, new_y = function(size, results.loc[i, 'fmap3CoordinatesX'], results.loc[i, 'fmap3CoordinatesY'], angle)
        new_results.loc[i, 'fmap3CoordinatesX'] = new_x
        new_results.loc[i, 'fmap3CoordinatesY'] = new_y

    return new_results

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
from sklearn.model_selection import train_test_split
import numpy as np
import copy
import pandas as pd
import math
from settings import *
from utils import *


def model_list(results, scenarios):
    model_list = []

    for index in range(len(scenarios)):
                
        scenario_results = results.loc[results["Scenario"] == (index+1)]
    
        scenario_list = []

        for index_res in range(len(scenario_results)):
        
            scenario_frame = copy.deepcopy(scenarios[index])
            scenario_frame["UAV"] = 0
        
            top_scenario = scenario_results.loc[scenario_results["topologyId"] == (index_res+1)]
            #scenario_frame["topologyId"] = (index_res+1)
            # UAV 1
            x_frame = scenario_frame['x'] == int(top_scenario['fmap1CoordinatesX'])
            y_frame = scenario_frame['y'] == int(top_scenario['fmap1CoordinatesY'])
            row_ind = scenario_frame[x_frame & y_frame].index
            scenario_frame.loc[row_ind, 'UAV'] = 1
            # UAV 2
            x_frame = scenario_frame['x'] == int(top_scenario['fmap2CoordinatesX'])
            y_frame = scenario_frame['y'] == int(top_scenario['fmap2CoordinatesY'])
            row_ind = scenario_frame[x_frame & y_frame].index
            scenario_frame.loc[row_ind, 'UAV'] = 1
            # UAV 3
            x_frame = scenario_frame['x'] == int(top_scenario['fmap3CoordinatesX'])
            y_frame = scenario_frame['y'] == int(top_scenario['fmap3CoordinatesY'])
            row_ind = scenario_frame[x_frame & y_frame].index
            scenario_frame.loc[row_ind, 'UAV'] = 1

            scenario_list.append(scenario_frame)

        model_list.append(scenario_list)

    return model_list


def datarate_matrix(scenario_frame):
    scenario_matrix = np.zeros((SCENARIO_ROWS, SCENARIO_COLUMNS), dtype = 'float')
    for i in range(len(scenario_frame)):
        x = scenario_frame.loc[i, 'x']
        y = scenario_frame.loc[i, 'y']
        rate = scenario_frame.loc[i, 'dataRateMbps']
        scenario_matrix[x][y] = rate
    
    return scenario_matrix    

def drones_matrix(results_line):
    matrix = np.zeros((SCENARIO_ROWS, SCENARIO_COLUMNS), dtype = 'float')
    drone1_x = int(results_line.loc['fmap1CoordinatesX'])
    drone1_y = int(results_line.loc['fmap1CoordinatesY'])
    drone2_x = int(results_line.loc['fmap2CoordinatesX'])
    drone2_y = int(results_line.loc['fmap2CoordinatesY'])
    drone3_x = int(results_line.loc['fmap3CoordinatesX'])
    drone3_y = int(results_line.loc['fmap3CoordinatesY'])
    quality_items = [float(results_line.loc['meanRxBitrateMbps']),float(results_line.loc['meanDelayMs']),
    float(results_line.loc['meanJitterMs']),float(results_line.loc['meanPdr'])]
    matrix[drone1_x][drone1_y] = 1
    matrix[drone2_x][drone2_y] = 1
    matrix[drone3_x][drone3_y] = 1
    return matrix, quality_items


def build_model_structure_transformation(model_structure, model_prediction, list_scenarios, list_topologies,function, angle):
    index_model_structure = 0
    model_structure_transformed = []
    model_prediction_transformed = []
    index_scenario = 0
    for scenario_id in list_scenarios:
        scenario_matrix = model_structure[index_model_structure][0]
        scenario_matrix_transformed = transform_matrix(scenario_matrix, function, angle)
        for topology_id in list_topologies[index_scenario]:
            topology_matrix = model_structure[index_model_structure][1]
            topology_matrix_transformed = transform_matrix(topology_matrix, function, angle)
            model_structure_transformed.append([scenario_matrix_transformed, topology_matrix_transformed])
            model_prediction_transformed.append(model_prediction[index_model_structure])
            index_model_structure += 1
        index_scenario += 1
    return model_structure_transformed, model_prediction_transformed

def build_model_structure(scenarios, results, list_scenarios, list_topologies):
    model_struct_orig = []
    model_prediction = []
    #first the topologies without any transformation
    index_scenario = 0
    for scenario_id in list_scenarios:
        scenario_begin_index = (scenario_id - 1) * SCENARIO_TOPOLOGIES_NO
        scenario_matrix = datarate_matrix(scenarios[scenario_id - 1])
        if(NORMALIZE_DATA == 1):
            scenario_matrix = normalize_matrix(scenario_matrix)
        for topology_id in list_topologies[index_scenario]:
            index_results = scenario_begin_index + topology_id - 1
            topology_matrix, qualities_list = drones_matrix(results.loc[index_results])
            if(DISTANCE_ENCODING == 1):
                topology_matrix = sparse_to_distance(topology_matrix)
            if(NORMALIZE_DATA == 1):
                topology_matrix = normalize_matrix(topology_matrix)
            model_struct_orig.append([scenario_matrix, topology_matrix])
            model_prediction.append(qualities_list)
        index_scenario += 1
    if(USE_TRANSFORMATIONS == 1):
        #Then the topologies with a 90 rotation
        model_struct_rot1, model_pred_rot1 = build_model_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, rotate, 90)
        #Then the topologies with a 180 rotation
        model_struct_rot2, model_pred_rot2 = build_model_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, rotate, 180)
        #Then the topologies with a 270 rotation
        model_struct_rot3, model_pred_rot3 = build_model_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, rotate, 270)
        #Then the topologies with a symmetry over the 0 axis
        model_struct_sym1, model_pred_sym1 = build_model_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, symmetric, 0)
        #Then the topologies with a symmetry over the 45 axis
        model_struct_sym2, model_pred_sym2 = build_model_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, symmetric, 45)
        #Then the topologies with a symmetry over the 90 axis
        model_struct_sym3, model_pred_sym3 = build_model_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, symmetric, 90)
        #Then the topologies with a symmetry over the 135 axis
        model_struct_sym4, model_pred_sym4 = build_model_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, symmetric, 135)

        return (model_struct_orig + model_struct_rot1 + model_struct_rot2 + model_struct_rot3 + model_struct_sym1 + model_struct_sym2 + model_struct_sym3 + model_struct_sym4),(model_prediction + model_pred_rot1 + model_pred_rot2 + model_pred_rot3 + model_pred_sym1 + model_pred_sym2 + model_pred_sym3 + model_pred_sym4)
    else:
        return model_struct_orig, model_prediction      
#Decided to not use this function in order to make the code more generic
def normalize_sparse_topology(matrix):
    new_matrix = np.empty((len(matrix), len(matrix[0])), dtype = "float")
    mean = (97*0+3*1)/100
    std = math.sqrt((97*(0-mean)*(0-mean)+3*(1-mean)*(1-mean))/100)

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            new_matrix[i][j] = (matrix[i][j] - mean)/std

    return new_matrix


def separate_qualities(qualities_list):
    throughput = []
    delay = []
    jitter = []
    pdr = []

    for index in range(len(qualities_list)):
        throughput.append(qualities_list[index][0])
        delay.append(qualities_list[index][1])
        jitter.append(qualities_list[index][2])
        pdr.append(qualities_list[index][3])


    return throughput, delay, jitter, pdr
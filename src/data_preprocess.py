import numpy as np
import settings
import utils
from random import *


def datarate_matrix(scenario_frame):
    scenario_matrix = np.zeros((settings.SCENARIO_ROWS, settings.SCENARIO_COLUMNS), dtype = 'float')
    for i in range(len(scenario_frame)):
        x = scenario_frame.loc[i, 'x']
        y = scenario_frame.loc[i, 'y']
        rate = scenario_frame.loc[i, 'dataRateMbps']
        scenario_matrix[y][x] = rate
    
    return scenario_matrix    

def drones_matrix(results_line):
    matrix = np.zeros((settings.SCENARIO_ROWS, settings.SCENARIO_COLUMNS), dtype = 'float')
    drone1_x = int(results_line.loc['fmap1CoordinatesX'])
    drone1_y = int(results_line.loc['fmap1CoordinatesY'])
    drone2_x = int(results_line.loc['fmap2CoordinatesX'])
    drone2_y = int(results_line.loc['fmap2CoordinatesY'])
    drone3_x = int(results_line.loc['fmap3CoordinatesX'])
    drone3_y = int(results_line.loc['fmap3CoordinatesY'])
    quality_items = [float(results_line.loc['meanRxBitrateMbps']),float(results_line.loc['meanDelayMs']),
    float(results_line.loc['meanJitterMs']),float(results_line.loc['meanPdr'])]
    matrix[drone1_y][drone1_x] = 1
    matrix[drone2_y][drone2_x] = 1
    matrix[drone3_y][drone3_x] = 1
    return matrix, quality_items


def build_input_structure_transformation(model_structure, model_prediction, list_scenarios, list_topologies,function, angle):
    index_model_structure = 0
    model_structure_transformed = []
    model_prediction_transformed = []
    index_scenario = 0
    for scenario_id in list_scenarios:
        if(len(list_topologies[index_scenario]) > 0):
            scenario_matrix = model_structure[index_model_structure][0]
            scenario_matrix_transformed = utils.transform_matrix(scenario_matrix, function, angle)
        for topology_id in list_topologies[index_scenario]:
            topology_matrix = model_structure[index_model_structure][1]
            topology_matrix_transformed = utils.transform_matrix(topology_matrix, function, angle)
            model_structure_transformed.append([scenario_matrix_transformed, topology_matrix_transformed])
            model_prediction_transformed.append(model_prediction[index_model_structure])
            index_model_structure += 1
        index_scenario += 1
    return model_structure_transformed, model_prediction_transformed

def build_input_structure(scenarios, results, list_scenarios, list_topologies):
    model_struct_orig = []
    model_prediction = []
    #first the topologies without any transformation
    index_scenario = 0
    for scenario_id in list_scenarios:
        scenario_begin_index = (scenario_id - 1) * settings.SCENARIO_TOPOLOGIES_NO
        scenario_matrix = datarate_matrix(scenarios[scenario_id - 1])
        if(settings.NORMALIZE_DATA == 1):
            mean, std = utils.stats_matrix(scenario_matrix)
        for topology_id in list_topologies[index_scenario]:
            index_results = scenario_begin_index + topology_id - 1
            topology_matrix, qualities_list = drones_matrix(results.loc[index_results])
            if(settings.DISTANCE_ENCODING == 1):
                topology_matrix = utils.sparse_to_distance(topology_matrix)
            if(settings.NORMALIZE_DATA == 1):
                topology_matrix = utils.normalize_matrix(topology_matrix, mean, std)
            model_struct_orig.append([scenario_matrix, topology_matrix])
            model_prediction.append(qualities_list)
        index_scenario += 1
    if(settings.USE_TRANSFORMATIONS == 1):
        #Then the topologies with a 90 rotation
        model_struct_rot1, model_pred_rot1 = build_input_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, utils.rotate, 90)
        #Then the topologies with a 180 rotation
        model_struct_rot2, model_pred_rot2 = build_input_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, utils.rotate, 180)
        #Then the topologies with a 270 rotation
        model_struct_rot3, model_pred_rot3 = build_input_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, utils.rotate, 270)
        #Then the topologies with a symmetry over the 0 axis
        model_struct_sym1, model_pred_sym1 = build_input_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, utils.symmetric, 0)
        #Then the topologies with a symmetry over the 45 axis
        model_struct_sym2, model_pred_sym2 = build_input_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, utils.symmetric, 45)
        #Then the topologies with a symmetry over the 90 axis
        model_struct_sym3, model_pred_sym3 = build_input_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, utils.symmetric, 90)
        #Then the topologies with a symmetry over the 135 axis
        model_struct_sym4, model_pred_sym4 = build_input_structure_transformation(model_struct_orig, model_prediction, list_scenarios, list_topologies, utils.symmetric, 135)

        return (model_struct_orig + model_struct_rot1 + model_struct_rot2 + model_struct_rot3 + model_struct_sym1 + model_struct_sym2 + model_struct_sym3 + model_struct_sym4),(model_prediction + model_pred_rot1 + model_pred_rot2 + model_pred_rot3 + model_pred_sym1 + model_pred_sym2 + model_pred_sym3 + model_pred_sym4)
    else:
        return model_struct_orig, model_prediction      

def build_input_struct_channels_last_matrix(input_entry):
    new_struct = np.empty((len(input_entry[0]), len(input_entry[0][0]), 2), dtype='float')
    for i in range(len(input_entry[0])):
        for j in range(len(input_entry[0][i])):
            new_struct[i][j] = [input_entry[0][i][j], input_entry[1][i][j]]
    return new_struct

def build_input_structure_channels_last(input_struct):
    new_struct = []
    for input_entry in input_struct:
        new_struct.append(build_input_struct_channels_last_matrix(input_entry))
    return new_struct

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

def build_topologie_train_list(scenarios):

    top_list = []

    for index in range(len(scenarios)):
        top_list.append(sample(range(1, settings.SCENARIO_TOPOLOGIES_NO), settings.TOPOLOGIES_TRAINING))

    return top_list


def build_topologie_validation_n_test_list(train_list):

    return_list = []
    validation_list = []
    test_list = []
    complete_list = list(range(1,(settings.SCENARIO_TOPOLOGIES_NO+1)))

    for index in range(len(train_list)):

        diff = list(set(complete_list) - set(train_list[index]))
        validation_list.append(diff[:settings.TOPOLOGIES_VALIDATION])
        test_list.append(diff[settings.TOPOLOGIES_VALIDATION:])

    return_list.append(validation_list)
    return_list.append(test_list)

    return return_list

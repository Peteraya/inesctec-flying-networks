import math
import random
import time
import numpy as np
import utils
import settings
import data_preprocess
random.seed(time.time())

def valid_position(position, nrows, ncolumns):
    if(position[0] < 0 or position[1] < 0):
        return False
    elif(position[0] >= nrows or position[1] >= ncolumns):
        return False
    else:
        return True

def adjacent_position(position, nrows, ncolumns):
    new_position = random.randint(0, 3)

    while(True):
        if(new_position % 4 == 0 and valid_position([position[0]+1, position[1]], nrows, ncolumns)):
            return [position[0]+1, position[1]]
        elif(new_position % 4 == 1 and valid_position([position[0]-1, position[1]], nrows, ncolumns)):
            return [position[0]-1, position[1]]
        elif(new_position % 4 == 2 and valid_position([position[0], position[1]+1], nrows, ncolumns)):
            return [position[0], position[1]+1]
        elif(new_position % 4 == 3 and valid_position([position[0], position[1]-1], nrows, ncolumns)):
            return [position[0], position[1]-1]
        new_position += 1

def adjacent_state(drones, nrows, ncolumns):
    new_drones = drones.copy()
    drone_index = random.randint(0, len(drones) - 1)
    new_drones[drone_index] = adjacent_position(drones[drone_index], nrows, ncolumns)
    return new_drones

def value(model_throughput, model_delay, model_pdr, scenario, topology):

    scenario_topologies_list = np.array([np.array([scenario, topology])])
    if(settings.CHANNELS_LAST):
        scenario_topologies_list = np.array(data_preprocess.build_input_structure_channels_last(scenario_topologies_list))
    throughput_pred = model_throughput.predict(scenario_topologies_list)
    delay_pred = model_delay.predict(scenario_topologies_list)
    pdr_pred = model_pdr.predict(scenario_topologies_list)
    return settings.quality(throughput_pred[0][0], delay_pred[0][0], pdr_pred[0][0]), [throughput_pred[0][0], delay_pred[0][0], pdr_pred[0][0]]

def get_topology(drones, mean, std, nrows, ncolumns):
    topology = np.zeros((nrows, ncolumns))
    for i in range(0, len(drones)):
        topology[int(drones[i][0])][int(drones[i][1])] = 1
    if(settings.DISTANCE_ENCODING):
        topology = utils.sparse_to_distance(topology)
    if(settings.NORMALIZE_DATA):
        topology = utils.normalize_matrix(topology, mean, std)
    return topology

def simulated_annealing(model_throughput, model_delay, model_pdr, scenario, drones):
    mean, std = utils.stats_matrix(scenario)
    nrows = len(scenario)
    ncolumns = len(scenario[0])
    topology = get_topology(drones, mean, std, nrows, ncolumns)
    current_value, variables = value(model_throughput, model_delay, model_pdr, scenario, topology)
    best_drones = drones.copy()
    best_value = current_value
    best_variables = variables.copy()
    temperature = 10000
    while(temperature > 0):
        print("Temperature: "+str(temperature))
        print("Drones Location: "+str(drones))
        print("Current State Value: "+str(current_value))
        print("Variables: "+str(variables))
        print("\n")
        new_drones = adjacent_state(drones, nrows, ncolumns)
        new_topology = get_topology(new_drones, mean, std, nrows, ncolumns)
        new_value, new_variables = value(model_throughput, model_delay, model_pdr, scenario, new_topology)
        diff = new_value - current_value
        if(diff >= 0):
            topology = np.copy(new_topology)
            current_value = new_value
            drones = new_drones
            variables = new_variables
            if(current_value > best_value):
                best_value = current_value
                best_drones = drones.copy()
                best_variables = variables.copy()
        else:
            probability = math.exp(10000*diff/temperature) 
            random_float = random.random()
            if(random_float < probability):
                topology = np.copy(new_topology)
                current_value = new_value
                drones = new_drones
                variables = new_variables
                if(current_value > best_value):
                    best_value = current_value
                    best_drones = drones.copy()
                    best_variables = variables.copy()
        temperature -= 1

    return best_drones, best_value, best_variables



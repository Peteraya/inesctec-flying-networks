import numpy as np
from settings import *
from utils import *
from keras.models import model_from_json


def save_topologies_to_json():
    topology = np.zeros((10, 10), dtype = 'float')
    topologies = []
    for d_1i in range(0, 10):
        print(str(d_1i)+"\n")
        for d_1j in range(0, 10):
            topology[d_1i][d_1j] = 1
            print("    "+str(d_1j)+"\n") 
            for d_2i in range(0, 10):
                for d_2j in range(0, 10):
                    topology[d_2i][d_2j] = 1 
                    for d_3i in range(0, 10):
                        for d_3j in range(0, 10):
                            topology[d_3i][d_3j] = 1
                            if(DISTANCE_ENCODING == 1):
                                topology = sparse_to_distance(topology)
                            if(NORMALIZE_DATA == 1):
                                topology = normalize_matrix(topology)
                            topologies.append(topology)    
                            topology = np.zeros((10, 10), dtype = 'float')
    with open("../DataSet/topologies.json", "w+") as json_file:
        json_file.write(topologies)                        

    

def load_topologies_from_json():
    json_file = open("../DataSet/topologies.json", "r")
    topologies = json_file.read()


def load_models():
    json_file_throughput = open('../DataSet/model_throughput.json', 'r')
    model_throughput_json = json_file_throughput.read()
    json_file_throughput.close()
    model_throughput = model_from_json(model_throughput_json)
    model_throughput.load_weights('../DataSet/model_throughput.hdf5')

    json_file_delay = open('../DataSet/model_delay.json', 'r')
    model_delay_json = json_file_delay.read()
    json_file_delay.close()
    model_delay = model_from_json(model_delay_json)
    model_delay.load_weights('../DataSet/model_delay.hdf5')

    json_file_pdr = open('../DataSet/model_pdr.json', 'r')
    model_pdr_json = json_file_pdr.read()
    json_file_pdr.close()
    model_pdr = model_from_json(model_pdr_json)
    model_pdr.load_weights('../DataSet/model_pdr.hdf5')

    return model_throughput, model_delay, model_pdr

def best_topology_brute_force(model_throughput, model_delay, model_pdr, scenario, topologies):
    mean, std = stats_matrix(scenario)
    scenario_topologies_list = []
    for i in range(0, len(topologies)):
        if(NORMALIZE_DATA == 1):
            topologies[i] = matrix_multiply_add(topologies[i], mean, std)
        scenario_topologies_list.append([scenario, topologies[i]])
    
    return best_topology(model_throughput, model_delay, model_pdr, scenario_topologies_list)

def best_topology_simulated_annealing():
    #TODO: IMPLEMENT
    pass

def best_topology(model_throughput, model_delay, model_pdr, scenario_topologies_list):

    throughput_pred = model_throughput.predict(scenario_topologies_list)
    delay_pred = model_delay.predict(scenario_topologies_list)
    pdr_pred = model_pdr.predict(scenario_topologies_list)

    quality_pred = [quality(t,d,p) for t, d, p in zip(throughput_pred, delay_pred, pdr_pred)]  
    
    topology_index = np.array(quality_pred).argmax(axis = 0)
    return scenario_topologies_list[topology_index][1]

line1 = np.array([3, 0, 0, 3, 0, 0, 3, 0, 0, 3])
line2 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
scenario = np.array([line1, line2, line2, line1, line2, line2, line1, line2, line2, line1])
model_throughput, model_delay, model_pdr = load_models()
topology = best_topology_brute_force(model_throughput, model_delay, model_pdr, scenario)
print(topology)
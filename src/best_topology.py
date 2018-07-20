import numpy as np
from settings import *
from utils import *
from simulated_annealing import *
from keras.models import model_from_json
import codecs, json
from load_data import *
from data_preprocess import *


def save_topologies_to_json():
    topology = np.zeros((10, 10), dtype = 'float')
    topologies = []
    SIZE = 10
    for d_1i in range(0, SIZE):
        print(str(d_1i)+"\n")
        for d_1j in range(0, SIZE):
            topology[d_1i][d_1j] = 1
            print("    "+str(d_1j)+"\n") 
            for d_2i in range(0, SIZE):
                for d_2j in range(0, SIZE):
                    topology[d_2i][d_2j] = 1 
                    for d_3i in range(0, SIZE):
                        for d_3j in range(0, SIZE):
                            topology[d_3i][d_3j] = 1
                            if(DISTANCE_ENCODING == 1):
                                topology = sparse_to_distance(topology)
                            if(NORMALIZE_DATA == 1):
                                topology = normalize_matrix(topology)
                            topology = round_matrix(topology, 4)
                            topologies.append(topology.tolist())    
                            topology = np.zeros((10, 10), dtype = 'float')
    json.dump(topologies, codecs.open("../DataSet/topologies.json", 'w', encoding='utf-8'), separators=(',',':'), sort_keys=True, indent=4)
    return topologies                       

    

def load_topologies_from_json():
    json_file = codecs.open("../DataSet/topologies.json", 'r', encoding='utf-8').read()
    topologies = json.loads(json_file)
    return topologies


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
    
    throughput_pred = model_throughput.predict(scenario_topologies_list)
    delay_pred = model_delay.predict(scenario_topologies_list)
    pdr_pred = model_pdr.predict(scenario_topologies_list)

    quality_pred = [quality(t,d,p) for t, d, p in zip(throughput_pred, delay_pred, pdr_pred)]  
    
    topology_index = np.array(quality_pred).argmax(axis = 0)
    return scenario_topologies_list[topology_index][1]


def save_drones_to_json(drones_list):

    drones = []

    if not(os.path.exists("../DataSet/Topologies-json")):
        fileId = 1
    else:
        allFiles = glob.glob("../DataSet/Topologies-json/best_top*.json")
        fileId = len(allFiles)+1

    filename = '../DataSet/Topologies-json/best_top' + str(fileId) + '.json'

    drones.append({"x" : drones_list[0][0]*30+15 , "y" : drones_list[0][1]*30+15 , "z" : 10, "wifiCellRange": 100, "wifiChannelNumber": 36})
    drones.append({"x" : drones_list[1][0]*30+15 , "y" : drones_list[1][1]*30+15 , "z" : 10, "wifiCellRange": 100, "wifiChannelNumber": 40})
    drones.append({"x" : drones_list[2][0]*30+15 , "y" : drones_list[2][1]*30+15 , "z" : 10, "wifiCellRange": 100, "wifiChannelNumber": 44})

    jsonString = json.dumps(drones, separators=('\t,\t', ' : '))

    jsonString = jsonString.replace('[{', '[\n\t{ ')
    jsonString = jsonString.replace('}\t,\t{', ' } ,\n\t{ ')
    jsonString = jsonString.replace('}]', ' }\n]')

    with open(filename, 'w') as f:
        f.write(jsonString)

def get_scenarios_list():
    scenarios = read_scenarios(DATASET_DIRECTORY)
    scenarios_list = []
    for scenario in scenarios:
        scenarios_list.append(datarate_matrix(scenario))
    return scenarios_list

def best_topology(scenario_id):
    scenario = get_scenarios_list()[scenario_id-1]
    model_throughput, model_delay, model_pdr = load_models()
    initial_drones = [[1.0, 1.0], [4.0, 4.0], [7.0, 7.0]]
    topology, quality, drones = simulated_annealing(model_throughput, model_delay, model_pdr, scenario, initial_drones)
    save_drones_to_json(drones,scenario_id)
    print(topology)
    print(quality)
    print(drones)
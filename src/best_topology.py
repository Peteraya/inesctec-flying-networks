import numpy as np
import csv
from settings import *
from utils import *
from simulated_annealing import *
from keras.models import model_from_json
import codecs, json
from load_data import *
from data_preprocess import *



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

def get_scenarios_list():
    scenarios = read_scenarios(DATASET_DIRECTORY)
    scenarios_list = []
    for scenario in scenarios:
        scenarios_list.append(datarate_matrix(scenario))
    return scenarios_list

def save_drones_to_json(drones_list,scenarioId):

    drones = []

    filename = '../DataSet/Topologies-json/Fmaps-Topology-' + str(scenarioId) + '.json'

    drones.append({"x" : drones_list[0][0]*30+15 , "y" : drones_list[0][1]*30+15 , "z" : 10, "wifiCellRange": 100, "wifiChannelNumber": 36})
    drones.append({"x" : drones_list[1][0]*30+15 , "y" : drones_list[1][1]*30+15 , "z" : 10, "wifiCellRange": 100, "wifiChannelNumber": 40})
    drones.append({"x" : drones_list[2][0]*30+15 , "y" : drones_list[2][1]*30+15 , "z" : 10, "wifiCellRange": 100, "wifiChannelNumber": 44})

    jsonString = json.dumps(drones, separators=('\t,\t', ' : '))

    jsonString = jsonString.replace('[{', '[\n\t{ ')
    jsonString = jsonString.replace('}\t,\t{', ' } ,\n\t{ ')
    jsonString = jsonString.replace('}]', ' }\n]')

    with open(filename, 'w') as f:
        f.write(jsonString)


def save_qualities_to_csv(*args):

    quali_dict = {"quality": args[0], "throughput": args[1], "Delay": args[2], "pdr": args[3]}

    with open('../DataSet/Topologies-json/Fmaps-Topology-'+ str(args[4]) + '-Qualities.csv', 'w') as f:
        w = csv.DictWriter(f, quali_dict.keys())
        w.writeheader()
        w.writerow(quali_dict)


def best_topology(scenario_id):
    scenario = get_scenarios_list()[scenario_id-1]
    model_throughput, model_delay, model_pdr = load_models()
    initial_drones = [[1.0, 1.0], [4.0, 4.0], [7.0, 7.0]]
    drones, final_value, [throughput, delay, pdr] = simulated_annealing(model_throughput, model_delay, model_pdr, scenario, initial_drones)
    pdr = min(1, pdr)
    save_drones_to_json(drones,scenario_id)
    print("Best drones position: "+str(drones))
    print("Quality: "+str(final_value))
    print("Throughput: "+str(throughput))
    print("Delay: "+str(delay))
    print("PDR: "+str(pdr))
    save_qualities_to_csv(quality,throughput, delay, pdr,scenario_id)

def best_topology_all_scenarios():
    for index in range(10):
        best_topology(index+1)

if __name__ == '__main__':
    best_topology_all_scenarios()
	

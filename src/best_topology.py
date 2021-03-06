"""
This module contains functions that allow the best topology for a certain scenario,
representing the traffic generated by the users, to be found.
"""
import csv
import json
from keras.models import model_from_json
import simulated_annealing
import settings
import load_data
import data_preprocess


def load_models():
    """
    Loads precompiled models from json and hdf5 files 
    """
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
    """
    Retrieves the list of predefined scenarios, representing the traffic generated by the users.
    """
    scenarios = load_data.read_scenarios(settings.DATASET_DIRECTORY)
    scenarios_list = []
    for scenario in scenarios:
        scenarios_list.append(data_preprocess.datarate_matrix(scenario))
    return scenarios_list

def save_drones_to_json(drones_list, scenario_id):
    """
    Saves the best drones location to a json file.
    """
    drones = []

    filename = '../DataSet/Topologies-json/Fmaps-Topology-' + str(scenario_id) + '.json'

    drones.append({"x" : drones_list[0][0]*30+15, "y" : drones_list[0][1]*30+15, "z" : 10, "wifiCellRange": 100, "wifiChannelNumber": 36})
    drones.append({"x" : drones_list[1][0]*30+15, "y" : drones_list[1][1]*30+15, "z" : 10, "wifiCellRange": 100, "wifiChannelNumber": 40})
    drones.append({"x" : drones_list[2][0]*30+15, "y" : drones_list[2][1]*30+15, "z" : 10, "wifiCellRange": 100, "wifiChannelNumber": 44})

    json_string = json.dumps(drones, separators=('\t,\t', ' : '))

    json_string = json_string.replace('[{', '[\n\t{ ')
    json_string = json_string.replace('}\t,\t{', ' } ,\n\t{ ')
    json_string = json_string.replace('}]', ' }\n]')

    with open(filename, 'w') as file:
        file.write(json_string)


def save_qualities_to_csv(*args):
    """
    Saves the qualities of the network (throughput, delay and pdr) to a csv file.
    """
    quali_dict = {"quality": args[0], "throughput": args[1], "Delay": args[2], "pdr": args[3]}

    with open('../DataSet/Topologies-json/Fmaps-Topology-'+ str(args[4]) + '-Qualities.csv', 'w') as file:
        dict_writer = csv.DictWriter(file, quali_dict.keys())
        dict_writer.writeheader()
        dict_writer.writerow(quali_dict)


def best_topology(scenario_id):
    """
    Finds the best topology, that is, the best drones location for a certain scenario.
    """
    scenario = get_scenarios_list()[scenario_id-1]
    model_throughput, model_delay, model_pdr = load_models()
    initial_drones = [[1.0, 1.0], [4.0, 4.0], [7.0, 7.0]]
    drones, final_value, [throughput, delay, pdr] = simulated_annealing.simulated_annealing(model_throughput, model_delay, model_pdr, scenario, initial_drones)
    pdr = min(1, pdr)
    save_drones_to_json(drones, scenario_id)
    print("Best drones position: "+str(drones))
    print("Quality: "+str(final_value))
    print("Throughput: "+str(throughput))
    print("Delay: "+str(delay))
    print("PDR: "+str(pdr))
    save_qualities_to_csv(settings.quality, throughput, delay, pdr, scenario_id)

def best_topology_all_scenarios():
    """
    Finds and saves to files the best topologies for all predefined scenarios.
    """
    for index in range(1):
        best_topology(index+1)

#If run as script calls function best_topology_all_scenarios
if __name__ == '__main__':
    best_topology_all_scenarios()
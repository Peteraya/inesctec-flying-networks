from sklearn.model_selection import train_test_split
import numpy as np
import copy
from settings import *


	# usar func para np array com [scenarioX, top1.....]


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


def scenario_array(scenario_frame):
    scenario_array = np.zeros((SCENARIO_ROWS, SCENARIO_COLUMNS), dtype = 'float')
    for i in range(len(scenario_frame)):
        x = scenario_frame.loc[i, 'x']
        y = scenario_frame.loc[i, 'y']
        rate = scenario_frame.loc[i, 'dataRateMbps']
        scenario_array[x][y] = rate
    
    return scenario_array    

def sparse_matrix(results_line):
    matrix = np.zeros((SCENARIO_ROWS, SCENARIO_COLUMNS), dtype = 'float')
    drone1_x = int(results_line.loc['fmap1CoordinatesX'])
    drone1_y = int(results_line.loc['fmap1CoordinatesY'])
    drone2_x = int(results_line.loc['fmap2CoordinatesX'])
    drone2_y = int(results_line.loc['fmap2CoordinatesY'])
    drone3_x = int(results_line.loc['fmap3CoordinatesX'])
    drone3_y = int(results_line.loc['fmap3CoordinatesY'])
    matrix[drone1_x][drone1_y] = 1
    matrix[drone2_x][drone2_y] = 1
    matrix[drone3_x][drone3_y] = 1
    return matrix

'''def build_model_structure(scenarios, results, list_scenarios, normalized):
    for i in range(list_scenarios):
        scenarios_id = '''


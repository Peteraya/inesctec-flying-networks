from sklearn.model_selection import train_test_split
import numpy as np
import copy
from load_data import *


abs_path = os.path.abspath(os.path.dirname(__file__))

if platform.system() == "Windows" :
	DATASET_DIRECTORY =  "../DataSet" 
else:
	DATASET_DIRECTORY = os.path.join(abs_path, "../DataSet")


results = read_results(DATASET_DIRECTORY)
scenarios = read_scenarios(DATASET_DIRECTORY)


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


	aux_model_list = pd.DataFrame()
	aux_model_list = pd.concat(scenario_list)
	model_list.append(scenario_list)



#model_dataframe = pd.DataFrame()
#model_dataframe = pd.concat(model_list)
#model_dataframe.to_csv('model_entry.csv', sep=',',index = False)
# sparse_matrix = np.zeros((10,10), dtype = 'int')
# sparse_matrix = np.matrix(sparse_matrix)

def scenario_array(scenario_frame):
    scenario_array = np.zeros((10, 10), dtype = 'int')
    for i in range(len(scenario_frame)):
        x = scenario_frame.loc[i, 'x']
        y = scenario_frame.loc[i, 'y']
        rate = scenario_frame.loc[i, 'dataRateMbps']
        scenario_array[x][y] = rate
    
    return scenario_array    



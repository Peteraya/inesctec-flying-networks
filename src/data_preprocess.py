from sklearn.model_selection import train_test_split
import numpy as np
import copy
from load_data import *


abs_path = os.path.abspath(os.path.dirname(__file__))

if platform.system() == "Windows" :
	DATASET_DIRECTORY =  "../DataSet" 
else:
	DATASET_DIRECTORY = os.path.join(abs_path, "../DataSet")



def create_model_dataframe(dataset_directory):

	results = read_results(dataset_directory)
	scenarios = read_scenarios(dataset_directory)

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



def create_topologies_matrix(dataset_directory):

	results = read_results(dataset_directory)
	scenarios = read_scenarios(dataset_directory)


	topologie = np.zeros((10,10), dtype = 'int')
	top_scenario = results.iloc[0]

	print(top_scenario['fmap1CoordinatesX'])
	#UVA 1
	x_frame = int(top_scenario['fmap1CoordinatesX'])
	y_frame = int(top_scenario['fmap1CoordinatesY'])
	topologie[x_frame][y_frame] = 1
	#UVA 2
	x_frame = int(top_scenario['fmap2CoordinatesX'])
	y_frame = int(top_scenario['fmap2CoordinatesY'])
	topologie[x_frame][y_frame] = 1
	#UVA 3
	x_frame = int(top_scenario['fmap3CoordinatesX'])
	y_frame = int(top_scenario['fmap3CoordinatesY'])
	topologie[x_frame][y_frame] = 1

	
	return topologie 

	# usar func para np array com [scenarioX, top1.....]
	


sparse_matrix = np.zeros((10,10), dtype = 'int')
#sparse_matrix = np.matrix(sparse_matrix)




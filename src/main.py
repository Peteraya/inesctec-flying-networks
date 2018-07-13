import sys
import os
from load_data import *
from data_preprocess import *
from model import *


abs_path = os.path.abspath(os.path.dirname(__file__))

if platform.system() == "Windows" :
	DATASET_DIRECTORY =  "../DataSet"
else:
	DATASET_DIRECTORY = os.path.join(abs_path, "../DataSet")

results = read_results(DATASET_DIRECTORY)
scenarios = read_scenarios(DATASET_DIRECTORY)


if DIVISION_BY_TOPOLOGIES:
	topologie_list_train = build_topologie_train_list(scenarios)
	aux_topologie_list = build_topologie_validation_n_test_list(topologie_list_train)
	topologie_list_validation = aux_topologie_list[0]
	topologie_list_test = aux_topologie_list[1]
	list_scenarios = list(range(1,(SCENARIOS_NO+1)))

	train_matrix, qualities_train = build_model_structure(scenarios, results, list_scenarios, topologie_list_train)
	validation_matrix, qualities_validation = build_model_structure(scenarios, results, list_scenarios, topologie_list_validation)
	test_matrix, qualities_test = build_model_structure(scenarios, results, list_scenarios, topologie_list_test)


else:
	topologies_list = []
	for index in range(10):
		topologies_list.append(list(range(1,(SCENARIO_TOPOLOGIES_NO+1))))

	train_matrix, qualities_train = build_model_structure(scenarios, results, SCENARIOS_TRAINING, topologies_list)
	validation_matrix, qualities_validation = build_model_structure(scenarios, results, SCENARIOS_VALIDATION, topologies_list)
	test_matrix, qualities_test = build_model_structure(scenarios, results, SCENARIOS_TEST, topologies_list)


model = build_model()
model.compile(optimizer = "adam", loss="mse", accuracy="rmse")


#model.fit(train_matrix, y_train,epochs=20, batch_size=1, verbose=1)

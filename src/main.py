import sys
import os
import numpy as np
from load_data import *
from data_preprocess import *
from models.base_model import *
from models.default_model import *



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

train_matrix = np.array(train_matrix)
throughput_train, delay_train, jitter_train, pdr_train = separate_qualities(qualities_train)
throughput_train, delay_train, jitter_train, pdr_train = np.array(throughput_train), np.array(delay_train), np.array(jitter_train), np.array(pdr_train)

validation_matrix = np.array(validation_matrix)
throughput_validation, delay_validation, jitter_validation, pdr_validation = separate_qualities(qualities_validation)
throughput_validation, delay_validation, jitter_validation, pdr_validation = np.array(throughput_validation), np.array(delay_validation), np.array(jitter_validation), np.array(pdr_validation)


model = DefaultModel()

#model.run(train_matrix, throughput_train, validation_matrix, throughput_validation, "Throughput")
#model.run(train_matrix, delay_train, validation_matrix, delay_validation, "Delay")
#model.run(train_matrix, jitter_train, validation_matrix, jitter_validation, "Jitter")
#model.run(train_matrix, pdr_train, validation_matrix, pdr_validation, "Pdr")

#  np.abs(throughput_validation - throughput_train.mean()).mean()        media 
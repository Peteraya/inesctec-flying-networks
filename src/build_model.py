import sys
import os
import numpy as np
from load_data import *
from data_preprocess import *
from models.base_model import *
import models.default_model
import models.channels_last_model



results = read_results(DATASET_DIRECTORY)
scenarios = read_scenarios(DATASET_DIRECTORY)


if DIVISION_BY_TOPOLOGIES:
	topologie_list_train = build_topologie_train_list(scenarios)
	aux_topologie_list = build_topologie_validation_n_test_list(topologie_list_train)
	topologie_list_validation = aux_topologie_list[0]
	topologie_list_test = aux_topologie_list[1]
	list_scenarios = list(range(1,(SCENARIOS_NO+1)))

	input_train, qualities_train = build_input_structure(scenarios, results, list_scenarios, topologie_list_train)
	input_validation, qualities_validation = build_input_structure(scenarios, results, list_scenarios, topologie_list_validation)
	input_test, qualities_test = build_input_structure(scenarios, results, list_scenarios, topologie_list_test)


else:
	topologies_list = []
	for index in range(10):
		topologies_list.append(list(range(1,(SCENARIO_TOPOLOGIES_NO+1))))

	input_train, qualities_train = build_input_structure(scenarios, results, SCENARIOS_TRAINING, topologies_list)
	input_validation, qualities_validation = build_input_structure(scenarios, results, SCENARIOS_VALIDATION, topologies_list)
	input_test, qualities_test = build_input_structure(scenarios, results, SCENARIOS_TEST, topologies_list)

if(CHANNELS_LAST == 1):
    input_train = build_input_structure_channels_last(input_train)
    input_validation = build_input_structure_channels_last(input_validation)


throughput_train, delay_train, jitter_train, pdr_train = separate_qualities(qualities_train)

throughput_validation, delay_validation, jitter_validation, pdr_validation = separate_qualities(qualities_validation)

if(VALIDATION_SPLIT == 1):
    input_train += input_validation
    throughput_train += throughput_validation
    delay_train += delay_validation
    jitter_train += jitter_validation
    pdr_train += pdr_validation
    input_validation = None
    throughput_validation = None
    delay_validation = None
    jitter_validation = None
    pdr_validation = None

input_train = np.array(input_train)
throughput_train, delay_train, jitter_train, pdr_train = np.array(throughput_train), np.array(delay_train), np.array(jitter_train), np.array(pdr_train)
input_validation = np.array(input_validation)
throughput_validation, delay_validation, jitter_validation, pdr_validation = np.array(throughput_validation), np.array(delay_validation), np.array(jitter_validation), np.array(pdr_validation)


if(CHANNELS_LAST == True):
    model_throughput = models.channels_last_model.ChannelsLastModel()
    model_delay = models.channels_last_model.ChannelsLastModel()
    model_jitter = models.channels_last_model.ChannelsLastModel()
    model_pdr = models.channels_last_model.ChannelsLastModel()
else:
    model_throughput = models.default_model.DefaultModel(0.001)
    model_delay = models.default_model.DefaultModel(0.001, True)
    model_jitter = models.default_model.DefaultModel(0.001)
    model_pdr = models.default_model.DefaultModel(0.001, True)

#model_throughput.run(input_train, throughput_train, input_validation, throughput_validation, "Throughput")
#model_delay.run(input_train, delay_train, input_validation, delay_validation, "Delay")
#model_jitter.run(input_train, jitter_train, input_validation, jitter_validation, "Jitter")
#model_pdr.run(input_train, pdr_train, input_validation, pdr_validation, "Pdr")


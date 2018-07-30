import sys
import os
import numpy as np
import load_data
import data_preprocess
import models.base_model
import models.default_model
import models.channels_last_model
import settings



results = load_data.read_results(settings.DATASET_DIRECTORY)
scenarios = load_data.read_scenarios(settings.DATASET_DIRECTORY)


if settings.DIVISION_BY_TOPOLOGIES:
    topologie_list_train = data_preprocess.build_topologie_train_list(scenarios)
    aux_topologie_list = data_preprocess.build_topologie_validation_n_test_list(topologie_list_train)
    topologie_list_validation = aux_topologie_list[0]
    topologie_list_test = aux_topologie_list[1]
    list_scenarios = list(range(1,(settings.SCENARIOS_NO+1)))

    input_train, qualities_train = data_preprocess.build_input_structure(scenarios, results, list_scenarios, topologie_list_train)
    input_validation, qualities_validation = data_preprocess.build_input_structure(scenarios, results, list_scenarios, topologie_list_validation)
    input_test, qualities_test = data_preprocess.build_input_structure(scenarios, results, list_scenarios, topologie_list_test)


else:
    topologies_list = []
    for index in range(10):
        topologies_list.append(list(range(1,(settings.SCENARIO_TOPOLOGIES_NO+1))))

    input_train, qualities_train = data_preprocess.build_input_structure(scenarios, results, settings.SCENARIOS_TRAINING, topologies_list)
    input_validation, qualities_validation = data_preprocess.build_input_structure(scenarios, results, settings.SCENARIOS_VALIDATION, topologies_list)
    input_test, qualities_test = data_preprocess.build_input_structure(scenarios, results, settings.SCENARIOS_TEST, topologies_list)

if(settings.CHANNELS_LAST == 1):
    input_train = data_preprocess.build_input_structure_channels_last(input_train)
    input_validation = data_preprocess.build_input_structure_channels_last(input_validation)
    input_test = data_preprocess.build_input_structure_channels_last(input_test)


throughput_train, delay_train, jitter_train, pdr_train = data_preprocess.separate_qualities(qualities_train)
throughput_validation, delay_validation, jitter_validation, pdr_validation = data_preprocess.separate_qualities(qualities_validation)
throughput_test, delay_test, jitter_test, pdr_test = data_preprocess.separate_qualities(qualities_test)

if(settings.VALIDATION_SPLIT == 1):
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
input_test = np.array(input_test)
throughput_test, delay_test, jitter_test, pdr_test = np.array(throughput_test), np.array(delay_test), np.array(jitter_test), np.array(pdr_test)

if(settings.CHANNELS_LAST == True):
    model_throughput = models.channels_last_model.ChannelsLastModel("Throughput")
    model_delay = models.channels_last_model.ChannelsLastModel("Delay")
    model_jitter = models.channels_last_model.ChannelsLastModel("Jitter")
    model_pdr = models.channels_last_model.ChannelsLastModel("Pdr")
else:
    model_throughput = models.default_model.DefaultModel(0.001, "Throughput")
    model_delay = models.default_model.DefaultModel(0.001, "Delay",True)
    model_jitter = models.default_model.DefaultModel(0.001, "Jitter")
    model_pdr = models.default_model.DefaultModel(0.001, "Pdr", True)

model_throughput.run(input_train, throughput_train, input_validation, throughput_validation, 100)
model_delay.run(input_train, delay_train, input_validation, delay_validation,100)
#model_jitter.run(input_train, jitter_train, input_validation, jitter_validation, 100)
model_pdr.run(input_train, pdr_train, input_validation, pdr_validation, 100)

if(settings.TEST_RESULTS == 1):
    model_throughput.evaluate(input_test, throughput_test)
    model_delay.evaluate(input_test, delay_test)
    model_pdr.evaluate(input_test, pdr_test)
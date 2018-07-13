import sys
import os
import numpy as np
from load_data import *
from data_preprocess import *
from models.base_model import *
from models.default_model import *


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

train_matrix = np.array(train_matrix)
throughput_train, delay_train, jitter_train, pdr_train = separate_qualities(qualities_train)
throughput_train, delay_train, jitter_train, pdr_train = np.array(throughput_train), np.array(delay_train), np.array(jitter_train), np.array(pdr_train)

validation_matrix = np.array(validation_matrix)
throughput_validation, delay_validation, jitter_validation, pdr_validation = separate_qualities(qualities_validation)
throughput_validation, delay_validation, jitter_validation, pdr_validation = np.array(throughput_validation), np.array(delay_validation), np.array(jitter_validation), np.array(pdr_validation)


model = DefaultModel()
model.run(train_matrix, throughput_train, validation_matrix, throughput_validation, "throughput")
model.run(train_matrix, delay_train, validation_matrix, delay_validation, "delay")
model.run(train_matrix, jitter_train, validation_matrix, jitter_validation, "jitter")
model.run(train_matrix, pdr_train, validation_matrix, pdr_validation, "pdr")
'''model = build_model()
model.compile(optimizer = "adam", loss="mse", metrics=['mae'])


train_matrix = np.array(train_matrix)
throughput_train, delay_train, jitter_train, pdr_train = separate_qualities(qualities_train)
throughput_train, delay_train, jitter_train, pdr_train = np.array(throughput_train), np.array(delay_train), np.array(jitter_train), np.array(pdr_train)

validation_matrix = np.array(validation_matrix)
throughput_validation, delay_validation, jitter_validation, pdr_validation = separate_qualities(qualities_validation)
throughput_validation, delay_validation, jitter_validation, pdr_validation = np.array(throughput_validation), np.array(delay_validation), np.array(jitter_validation), np.array(pdr_validation)

test_matrix = np.array(test_matrix)
throughput_test, delay_test, jitter_test, pdr_test = separate_qualities(qualities_test)
throughput_test, delay_test, jitter_test, pdr_test = np.array(throughput_test), np.array(delay_test), np.array(jitter_test), np.array(pdr_test)


# throughput
model.fit(train_matrix, throughput_train, epochs=20, batch_size=1, verbose=1)

y_pred = model.predict(test_matrix)

score_valid = model.evaluate(validation_matrix, throughput_validation,verbose=1)
print("Validation score throughput: ", score_valid)

score_test = model.evaluate(test_matrix, throughput_test,verbose=1)
print("Test score throughput: ", score_test)

print("----------------------------------------------------")

# delay
model.fit(train_matrix, delay_train, epochs=20, batch_size=1, verbose=1)

y_pred = model.predict(test_matrix)

score_valid = model.evaluate(validation_matrix, delay_validation,verbose=1)
print("Validation score delay: ", score_valid)

score_test = model.evaluate(test_matrix, delay_test,verbose=1)
print("Test score delay: ", score_test)

print("----------------------------------------------------")


# jitter
model.fit(train_matrix, jitter_train, epochs=20, batch_size=1, verbose=1)

y_pred = model.predict(test_matrix)

score_valid = model.evaluate(validation_matrix, jitter_validation,verbose=1)
print("Validation score jitter: ", score_valid)

score_test = model.evaluate(test_matrix, jitter_test,verbose=1)
print("Test score jitter: ", score_test)

print("----------------------------------------------------")


# pdr
model.fit(train_matrix, pdr_train, epochs=20, batch_size=1, verbose=1)

y_pred = model.predict(test_matrix)

score_valid = model.evaluate(validation_matrix, pdr_validation,verbose=1)
print("Validation score pdr: ", score_valid)

score_test = model.evaluate(test_matrix, pdr_test,verbose=1)
print("Test score pdr: ", score_test)'''
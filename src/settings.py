import sys
import os
import platform

#Global Variables
SCENARIO_ROWS = 10
SCENARIO_COLUMNS = 10
SCENARIO_TOPOLOGIES_NO = 200
SCENARIOS_NO = 10
TOPOLOGIES_TRAINING = 128
TOPOLOGIES_VALIDATION = 40
TOPOLOGIES_TESTING = 32
#SCENARIOS_TRAINING = [1, 2, 4, 6, 7, 10]
#SCENARIOS_VALIDATION = [5, 9]
SCENARIOS_TRAINING = [1, 2, 4, 6, 7, 10, 5, 9]
SCENARIOS_TEST = [3, 8]
SCENARIOS_VALIDATION = []
DIVISION_BY_TOPOLOGIES = 1
DISTANCE_ENCODING = 1
NORMALIZE_DATA = 1
USE_TRANSFORMATIONS = 1
CHANNELS_LAST = 0
VALIDATION_SPLIT = 0
USE_CALLBACKS = 1
TEST_RESULTS = 0


def quality(throughput, delay, pdr):
    return throughput - delay / 500 +pdr

abs_path = os.path.abspath(os.path.dirname(__file__))

if platform.system() == "Windows" :
	DATASET_DIRECTORY =  "../DataSet"
else:
	DATASET_DIRECTORY = os.path.join(abs_path, "../DataSet")
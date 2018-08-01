import os
import platform

#Global Variables
SCENARIO_ROWS = 10
SCENARIO_COLUMNS = 10
SCENARIO_TOPOLOGIES_NO = 200
SCENARIOS_NO = 10
TOPOLOGIES_TRAINING = 128
TOPOLOGIES_VALIDATION = 32
TOPOLOGIES_TESTING = 40
SCENARIOS_TRAINING = [1, 2, 4, 6, 7, 10]
SCENARIOS_VALIDATION = [5, 9]
SCENARIOS_TEST = [3, 8]
DIVISION_BY_TOPOLOGIES = False
DISTANCE_ENCODING = True
NORMALIZE_DATA = True
USE_TRANSFORMATIONS = True
CHANNELS_LAST = False
USE_CALLBACKS = False
TEST_RESULTS = True


def quality(throughput, delay, pdr):
    return throughput - delay / 500 +pdr

def get_dataset_directory():
    if platform.system() == "Windows":
        return "../DataSet"
    else:
        abs_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(abs_path, "../DataSet")

DATASET_DIRECTORY = get_dataset_directory()

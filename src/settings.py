"""
This module contains the generic settings of our program, that will change 
the way our model will be compileand way data will be fit into it.
"""
import os
import platform

#Settings
SCENARIO_ROWS = 10 #Number of rows in each scenario
SCENARIO_COLUMNS = 10 #Number of columns in each scenario
SCENARIO_TOPOLOGIES_NO = 200 #Number of topologies by scenario
SCENARIOS_NO = 10 #Number of scenarios
TOPOLOGIES_TRAINING = 128 #Number of topologies to be used in training
TOPOLOGIES_VALIDATION = 32 #Number of topologies to be used in validation
TOPOLOGIES_TESTING = 40 #Number of topologies to be used in testing
SCENARIOS_TRAINING = [1, 2, 4, 6, 7, 10] #Scenarios to be used in training
SCENARIOS_VALIDATION = [5, 9] #Scenarios to be used in validation
SCENARIOS_TEST = [3, 8] #Scenarios to be used in testing
DIVISION_BY_TOPOLOGIES = False #True if division train/validation/test is to be made by topologies
DISTANCE_ENCODING = True #True if the topologies should use distance encoding
NORMALIZE_DATA = True #True if data should be normalized
USE_TRANSFORMATIONS = True #True if data augmentation should be used
CHANNELS_LAST = True #True if data to be fit to the model should have channels_last format
USE_CALLBACKS = True #True if callbacks should be used when training the model
TEST_RESULTS = True #True if the program should present the results of the tests


def quality(throughput, delay, pdr):
    """
    Computes the quality of a network
    """
    return throughput - delay / 500 +pdr

def get_dataset_directory():
    """
    Auxiliary function that returns the dataset directory which is different according to the platform:
    Windows or Linux
    """
    if platform.system() == "Windows":
        return "../DataSet"
    else:
        abs_path = os.path.abspath(os.path.dirname(__file__))
        return os.path.join(abs_path, "../DataSet")

DATASET_DIRECTORY = get_dataset_directory() #Path of the dataset directory

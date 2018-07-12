import sys
import os
from load_data import *
from data_preprocess import *

def main():
    abs_path = os.path.abspath(os.path.dirname(__file__))

    if platform.system() == "Windows" :
        DATASET_DIRECTORY =  "../DataSet"
    else:
        DATASET_DIRECTORY = os.path.join(abs_path, "../DataSet")
    results = read_results(DATASET_DIRECTORY)
    scenarios = read_scenarios(DATASET_DIRECTORY)

main()
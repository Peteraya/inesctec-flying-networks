import pandas as pd
import glob
import sys
import os
import platform
from utils import *



def create_results(dataset_directory):
    results_directory = os.path.join(dataset_directory, "Results/Scenario-")
    path =results_directory
    results_list = []
    for index_scn in range(10):
        new_path = path + str(index_scn+1)+'/'
        print(new_path)
        list_scenario = []
        for index in range(200):
            allFiles = glob.glob(new_path + "/Results-"+str(index + 1)+"-*.csv")
            frame = pd.DataFrame()
            list_ = []
            for index in range(len(allFiles)):
                df = pd.read_csv(allFiles[index], index_col = False, header=0)
                list_.append(df)

            frame = pd.concat(list_)
            list_scenario.append(frame[0:10].describe().loc[['mean']])
        scenario = []
        scenario = pd.concat(list_scenario)
        del scenario['nSimulationRun']
        scenario["Scenario"] = str(index_scn+1)
        results_list.append(scenario)

    results = pd.DataFrame()
    results = pd.concat(results_list)
    results.loc[:, 'fmap1CoordinatesX'] = (results.loc[:, 'fmap1CoordinatesX'] - 15) / 30
    results.loc[:, 'fmap2CoordinatesX'] = (results.loc[:, 'fmap2CoordinatesX'] - 15) / 30
    results.loc[:, 'fmap3CoordinatesX'] = (results.loc[:, 'fmap3CoordinatesX'] - 15) / 30
    results.loc[:, 'fmap1CoordinatesY'] = (results.loc[:, 'fmap1CoordinatesY'] - 15) / 30
    results.loc[:, 'fmap2CoordinatesY'] = (results.loc[:, 'fmap2CoordinatesY'] - 15) / 30
    results.loc[:, 'fmap3CoordinatesY'] = (results.loc[:, 'fmap3CoordinatesY'] - 15) / 30

    results_file = os.path.join(dataset_directory, "results.csv")
    results.to_csv(results_file, sep=',',index = False)
    return None


def read_results(dataset_directory):
    results_file = os.path.join(dataset_directory, "results.csv")
    if not(os.path.isfile(results_file)):
        create_results(dataset_directory)

    results = pd.read_csv(results_file, index_col = False, sep=',')

    return results


#create_results('../DataSet/Results/Scenario-')

def read_scenarios(dataset_directory):
    scenarios = []
    for i in range(1, 11):
        scenario_directory = os.path.join(dataset_directory, "Results/Scenario-"+str(i))
        csv_file = os.path.join(scenario_directory, "Users-Topology-"+str(i)+".csv")
        scenario_frame = pd.read_csv(csv_file)
        for j in range(0, len(scenario_frame)):
            scenario_frame.loc[j, 'x'] = int((scenario_frame.loc[j, 'x']-15)/30)
            scenario_frame.loc[j, 'y'] = int((scenario_frame.loc[j, 'y']-15)/30)
        scenarios.append(scenario_frame)
    return scenarios


abs_path = os.path.abspath(os.path.dirname(__file__))

if platform.system() == "Windows" :
    DATASET_DIRECTORY =  "../DataSet"
else:
    DATASET_DIRECTORY = os.path.join(abs_path, "../DataSet")




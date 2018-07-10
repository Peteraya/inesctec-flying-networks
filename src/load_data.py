import pandas as pd
import glob
import sys
import os
import platform
from utils import * 


def create_results(results_directory):
    path =results_directory
    results_list = []
    results = pd.DataFrame()

    for index_scn in range(10):
    	new_path = path + str(index_scn+1)+'/'
    	print(new_path)
    	allFiles = glob.glob(new_path + "/Results-*.csv")
    	frame = pd.DataFrame()
    	list_ = []

    	for index in range(len(allFiles)):
    		df = pd.read_csv(allFiles[index], index_col = False, header=0)
    		list_.append(df)

    	frame = pd.concat(list_)
    	scenario = []
    	list_ = []
    	begin=0
    	end=10

    	for index in range(200):
    		list_.append(frame[begin:end].describe().loc[['mean']])
    		begin+=10
    		end+=10

    	scenario = pd.concat(list_)
    	del scenario['nSimulationRun']
    	scenario["Scenario"] = str(index_scn+1)
    	results_list.append(scenario)


    results = pd.concat(results_list)
    results.to_csv('../DataSet/results.csv', sep=',',index = False)
    return None


def read_results(dataset_directory):
    results_directory = os.path.join(dataset_directory, "Results/Scenario-")
    results_file = os.path.join(dataset_directory, "results.csv")
    if not(os.path.isfile(results_file)):
    	create_results(results_directory)

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




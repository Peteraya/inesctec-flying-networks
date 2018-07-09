import pandas as pd
import glob
import sys
import os
from utils import * 

""" 
if os.path.isfile("../DataSet/results.csv"):
	print("Existe")

else:
	print("nope")
	"""

def create_results(dataset_directory):
    path =dataset_directory
    results_list = []
    results = pd.DataFrame()

    for index_scn in range(10):
    	new_path = path + str(index_scn+1)+'/'
    	print(new_path)
    	allFiles = glob.glob(new_path + "/*.csv")
    	frame = pd.DataFrame()
    	list_ = []

    	for index in range(len(allFiles)-1):
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



   
#create_results('../DataSet/Results/Scenario-')
#results = pd.read_csv('../DataSet/results.csv', index_col = False, sep=',')



def read_scenarios(dataset_directory):
    '''abs_path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(abs_path, "../DataSet")'''
    scenarios = []
    for i in range(1, 11):
        scenario_directory = os.path.join(dataset_directory, "Scenario-"+str(i))
        csv_file = os.path.join(scenario_directory, "Users-Topology-"+str(i)+".csv")
        scenario_frame = pd.read_csv(csv_file)
        for j in range(0, len(scenario_frame)):
            scenario_frame.loc[j, 'x'] = int((scenario_frame.loc[j, 'x']-15)/30)
            scenario_frame.loc[j, 'y'] = int((scenario_frame.loc[j, 'y']-15)/30)
        scenarios.append(scenario_frame)
    return scenarios

#DATASET_DIRECTORY = "/home/francisco/Desktop/Estagio_INESCTEC/INESCTEC-FLYINGNETWORKS/DataSet"
abs_path = os.path.abspath(os.path.dirname(__file__))
DATASET_DIRECTORY = os.path.join(abs_path, "../DataSet")

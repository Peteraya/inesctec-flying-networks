import pandas as pd
import glob
import sys
import os


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



    

create_results('../DataSet/Results/Scenario-')
results = pd.read_csv('../DataSet/results.csv', index_col = False, sep=',')

print(results)



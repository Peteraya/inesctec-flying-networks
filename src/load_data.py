import pandas as pd
import glob
import sys
import os

path =r'Results/Scenario-1/' # use your path
allFiles = glob.glob(path + "/*.csv")

frame = pd.DataFrame()
list_ = []
for index in range(len(allFiles)-1):
   df = pd.read_csv(allFiles[index],index_col=None, header=0)
   list_.append(df)

frame = pd.concat(list_)


print(frame)

#single_result = pd.read_csv("Results/Scenario-1/Results-1-1.csv", sep=',')
#print(single_result)

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

DATASET_DIRECTORY = "/home/francisco/Desktop/Estagio_INESCTEC/INESCTEC-FLYINGNETWORKS/DataSet"
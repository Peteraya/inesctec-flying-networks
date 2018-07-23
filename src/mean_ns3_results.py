import pandas as pd
import glob
import os

def mean_ns3_results(scenario_number):
    path = "scratch/uavs-and-ml/Results/Topologies-json/Scenario-" + str(scenario_number)
    results_list = []
    allFiles = glob.glob(path + "/Results-"+str(scenario_number)+"-*.csv")
    frame = pd.DataFrame()
    list_ = []
    for index in range(len(allFiles)):
        df = pd.read_csv(allFiles[index], index_col = False, header=0)
        list_.append(df)

    frame = pd.concat(list_)
    results_list.append(frame.describe().loc[['mean']])

    results = pd.DataFrame()
    results = pd.concat(results_list)

    results_file = os.path.join(path, "results_" + str(scenario_number) +".csv")
    results.to_csv(results_file, sep=',',index = False)
    return None
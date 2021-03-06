"""
This module loads data from files
"""
import glob
import os
import pandas as pd
import settings



def create_results(dataset_directory):
    """
    Groups results in a single file so that it becomes faster to load the data 
    """
    results_directory = os.path.join(dataset_directory, "Results/Scenario-")
    path = results_directory
    results_list = []
    for index_scn in range(settings.SCENARIOS_NO):
        new_path = path + str(index_scn+1)+'/'
        list_scenario = []
        for index in range(settings.SCENARIO_TOPOLOGIES_NO):
            all_files = glob.glob(new_path + "/Results-"+str(index + 1)+"-*.csv")
            frame = pd.DataFrame()
            list_ = []
            for index in range(len(all_files)):
                result_frame = pd.read_csv(all_files[index], index_col = False, header=0)
                list_.append(result_frame)

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
    """
    Loads results, grouping all the results together in a single file, if that file does not exists
    or loading the results from the already existing results single file
    """
    results_file = os.path.join(dataset_directory, "results.csv")
    if not(os.path.isfile(results_file)):
        create_results(dataset_directory)

    results = pd.read_csv(results_file, index_col = False, sep=',')

    return results


def read_scenarios(dataset_directory):
    """
    Loads data relative to the scenarios used
    """
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







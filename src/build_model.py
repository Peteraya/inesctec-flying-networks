"""
This module calls the functions in the files load_data.py and data_preprocess.py and in the folder models,
so that a model used to predict different variables of a network can be built.
"""
import load_data
import data_preprocess
import models.base_model
import models.default_model
import models.channels_last_model
import settings


def load_dataset():
    """
    Loads data.
    """
    results = load_data.read_results(settings.DATASET_DIRECTORY)
    scenarios = load_data.read_scenarios(settings.DATASET_DIRECTORY)


    if settings.DIVISION_BY_TOPOLOGIES:
        topologies_list_train = data_preprocess.build_topologies_train_list(scenarios)
        aux_topologies_list = data_preprocess.build_topologies_validation_n_test_list(topologies_list_train)
        topologies_list_validation = aux_topologies_list[0]
        topologies_list_test = aux_topologies_list[1]
        list_scenarios = list(range(1,(settings.SCENARIOS_NO+1)))

        input_train, qualities_train = data_preprocess.build_input_structure(scenarios, results, list_scenarios, topologies_list_train)
        input_validation, qualities_validation = data_preprocess.build_input_structure(scenarios, results, list_scenarios, topologies_list_validation)
        input_test, qualities_test = data_preprocess.build_input_structure(scenarios, results, list_scenarios, topologies_list_test)


    else:
        topologies_list = []
        for _index in range(10):
            topologies_list.append(list(range(1, (settings.SCENARIO_TOPOLOGIES_NO+1))))

        input_train, qualities_train = data_preprocess.build_input_structure(scenarios, results, settings.SCENARIOS_TRAINING, topologies_list)
        input_validation, qualities_validation = data_preprocess.build_input_structure(scenarios, results, settings.SCENARIOS_VALIDATION, topologies_list)
        input_test, qualities_test = data_preprocess.build_input_structure(scenarios, results, settings.SCENARIOS_TEST, topologies_list)

    if settings.CHANNELS_LAST:
        input_train = data_preprocess.build_input_structure_channels_last(input_train)
        input_validation = data_preprocess.build_input_structure_channels_last(input_validation)
        input_test = data_preprocess.build_input_structure_channels_last(input_test)


    throughput_train, delay_train, _jitter_train, pdr_train = data_preprocess.separate_qualities(qualities_train)
    throughput_validation, delay_validation, _jitter_validation, pdr_validation = data_preprocess.separate_qualities(qualities_validation)
    throughput_test, delay_test, _jitter_test, pdr_test = data_preprocess.separate_qualities(qualities_test)


    #input_train = np.array(input_train)
    #throughput_train, delay_train, jitter_train, pdr_train = np.array(throughput_train), np.array(delay_train), np.array(jitter_train), np.array(pdr_train)
    #input_validation = np.array(input_validation)
    #throughput_validation, delay_validation, jitter_validation, pdr_validation = np.array(throughput_validation), np.array(delay_validation), np.array(jitter_validation), np.array(pdr_validation)
    #input_test = np.array(input_test)
    #throughput_test, delay_test, jitter_test, pdr_test = np.array(throughput_test), np.array(delay_test), np.array(jitter_test), np.array(pdr_test)
    return [input_train, throughput_train, delay_train, pdr_train], [input_validation, throughput_validation, delay_validation, pdr_validation], [input_test, throughput_test, delay_test, pdr_test] 


def build_model():
    """
    This functions loads the dataset, compiles the model,
    fits the dataset to the model and also tests it if corresponding option in settings is turned on.
    """
    train_data, validation_data, test_data = load_dataset()
    if settings.CHANNELS_LAST:
        model_throughput = models.channels_last_model.ChannelsLastModel("Throughput")
        model_delay = models.channels_last_model.ChannelsLastModel("Delay")
        model_pdr = models.channels_last_model.ChannelsLastModel("Pdr")
    else:
        model_throughput = models.default_model.DefaultModel(0.001, "Throughput")
        model_delay = models.default_model.DefaultModel(0.001, "Delay",True)
        model_pdr = models.default_model.DefaultModel(0.001, "Pdr", True)

    model_throughput.run(train_data[0], train_data[1], validation_data[0], validation_data[1], 2)
    model_delay.run(train_data[0], train_data[2], validation_data[0], validation_data[2],2)
    model_pdr.run(train_data[0], train_data[3], validation_data[0], validation_data[3], 2)

    if settings.TEST_RESULTS:
        model_throughput.evaluate(test_data[0], test_data[1])
        model_delay.evaluate(test_data[0], test_data[2])
        model_pdr.evaluate(test_data[0], test_data[3])

#If run as script, builds model
if __name__ == '__main__':
    build_model()

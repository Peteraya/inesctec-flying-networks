import glob
import os 
from keras.utils import plot_model
from keras.models import Model
from keras.callbacks import ModelCheckpoint
import numpy as np
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod
import settings
import utils

class BaseModel:
    @abstractmethod
    def __init__(self):
        pass

    def print_model(self, filename):
        plot_model(self.model, to_file = '../DataSet/'+filename)
    
    def save_json(self, variable_name):
        allFiles = glob.glob("../DataSet/Models-json/model_"+variable_name+"*.json")
        new_id = len(allFiles) + 1
        model_json = self.model.to_json() 
        with open("../DataSet/Models-json/model_"+variable_name+str(new_id)+".json", "w+") as json_file:
            json_file.write(model_json)



    def run(self, input_train, y_train, input_validation, y_validation, variable_name):

        if not(os.path.exists("../DataSet/Checkpoints")):
            fileId = 1
        else:
            allFiles = glob.glob("../DataSet/Checkpoints/checkpoint*.hdf5")
            fileId = len(allFiles)+1

        if not(os.path.exists("../DataSet/Plots/"+variable_name)):
            plotId = 1
        else:
            allFiles = glob.glob("../DataSet/Plots/"+variable_name+"/plot*")
            plotId = int(len(allFiles)/2) + 1


        checkpointer = ModelCheckpoint(filepath='../DataSet/Checkpoints/checkpoint' + str(fileId) + ".hdf5", verbose=1, save_best_only=True)
    
        if(settings.VALIDATION_SPLIT == 0):
            history = self.model.fit(input_train, y_train, epochs=settings.NEPOCHS, batch_size=128, verbose=1, validation_data = (input_validation, y_validation), shuffle=True,callbacks=[checkpointer])
        else:
            input_train, y_train = utils.shuffle_input_data(input_train, y_train)
            history = self.model.fit(input_train, y_train, epochs=settings.NEPOCHS, batch_size=128, verbose=1, validation_split = 0.2, shuffle=True,callbacks=[checkpointer])

        self.save_json(variable_name)
        # list all data in history
        print(history.history.keys())
        # summarize history for mean absolute error
        plt.plot(history.history['mean_absolute_error'])
        plt.plot(history.history['val_mean_absolute_error'])
        plt.title('model mae')
        plt.ylabel('mae')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.savefig('../DataSet/Plots/' + variable_name + '/plot' + str(plotId) + "_mae.png")
        plt.show()
        # summarize history for loss
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.savefig('../DataSet/Plots/' + variable_name + '/plot' + str(plotId) + "_loss.png")
        plt.show()
        
        if(settings.VALIDATION_SPLIT == 0):
            score_valid = self.model.evaluate(input_validation, y_validation,verbose=1)
            print("----------------------------------------------------")
            print("Validation score "+ variable_name + ": ", score_valid)
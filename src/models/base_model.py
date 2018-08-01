import glob
import os 
from keras.utils import plot_model
from keras.models import Model
from keras.callbacks import ModelCheckpoint
import numpy as np
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod
import settings
from keras import backend

def mean_absolute_percentage_error(y_true, y_pred):
    return 100*backend.mean(abs((y_true-y_pred)/y_true), axis=-1)

class BaseModel:
    @abstractmethod
    def __init__(self):
        pass

    def print_model(self, filename):
        plot_model(self.model, to_file = '../DataSet/'+filename)
    
    def save_json(self, variable_name):
        all_files = glob.glob("../DataSet/Models-json/model_"+variable_name+"*.json")
        new_id = len(all_files) + 1
        model_json = self.model.to_json() 
        with open("../DataSet/Models-json/model_"+variable_name+str(new_id)+".json", "w+") as json_file:
            json_file.write(model_json)
    
    def save_plots(self, history):
        if not(os.path.exists("../DataSet/Plots/"+self.variable_name)):
            plot_id = 1
        else:
            all_files = glob.glob("../DataSet/Plots/"+self.variable_name+"/plot*")
            plot_id = int(len(all_files)/2) + 1
        
        # summarize history for mean absolute error
        plt.plot(history.history['mean_absolute_error'])
        plt.plot(history.history['val_mean_absolute_error'])
        plt.title('model mae')
        plt.ylabel('mae')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.savefig('../DataSet/Plots/' + self.variable_name + '/plot' + str(plot_id) + "_mae.png")
        plt.show()
        # summarize history for loss
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.savefig('../DataSet/Plots/' + self.variable_name + '/plot' + str(plot_id) + "_loss.png")
        plt.show()   
        

    def run(self, input_train, y_train, input_validation, y_validation, n_epochs):
        
        validation_empty = len(input_validation) == 0

        if not(os.path.exists("../DataSet/Checkpoints")):
            file_id = 1
        else:
            all_files = glob.glob("../DataSet/Checkpoints/checkpoint*.hdf5")
            file_id = len(all_files)+1
       
        if(settings.USE_CALLBACKS):
            checkpointer = ModelCheckpoint(filepath='../DataSet/Checkpoints/checkpoint' + str(file_id) + '.hdf5', verbose=1, save_best_only=True)
            model_callbacks = [checkpointer]
        else:
            model_callbacks = None
    
        if(not(validation_empty)):
            history = self.model.fit(input_train, y_train, epochs=n_epochs, batch_size=128, verbose=1, validation_data = (input_validation, y_validation), shuffle=True,callbacks=model_callbacks)
        else:
            history = self.model.fit(input_train, y_train, epochs=n_epochs, batch_size=128, verbose=1, shuffle=True,callbacks=model_callbacks)
        

        if(not(settings.USE_CALLBACKS)):
            self.model.save_weights('../DataSet/Checkpoints/checkpoint' + str(file_id) + '.hdf5')
            
        self.save_json(self.variable_name)
        # list all data in history
        print(history.history.keys())
        if(not(validation_empty)):
            self.save_plots(history)
        
        if(not(validation_empty)):
            self.evaluate(input_validation, y_validation)
        
    def evaluate(self, input_test, y_test):
        score = self.model.evaluate(input_test, y_test,verbose=1)
        print("----------------------------------------------------")
        print("Score "+ self.variable_name + ": ", score)
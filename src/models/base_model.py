import glob
import os 
from keras.utils import plot_model
from keras.models import Model
from keras.callbacks import ModelCheckpoint
import numpy as np
import matplotlib.pyplot as plt
from abc import ABCMeta, abstractmethod

class BaseModel:
    @abstractmethod
    def __init__(self):
        pass

    def print_model(self, filename):
        plot_model(self.model, to_file = '../../DataSet'+filename)

    def run(self, train_matrix, train_y, validation_matrix, validation_y, variable_name):

        if not(os.path.exists("../DataSet/Checkpoints")):
            fileId = 1
        else:
            allFiles = glob.glob("../DataSet/Checkpoints/checkpoint*.hdf5")
            fileId = len(allFiles)+1


        checkpointer = ModelCheckpoint(filepath='../DataSet/Checkpoints/checkpoint' + str(fileId) + ".hdf5", verbose=1, save_best_only=True)
    
        history = self.model.fit(train_matrix, train_y, epochs=10, batch_size=128, verbose=1, validation_split=0.2, shuffle=True,callbacks=[checkpointer])
        # list all data in history
        print(history.history.keys())
        # summarize history for mean absolute error
        plt.plot(history.history['mean_absolute_error'])
        plt.plot(history.history['val_mean_absolute_error'])
        plt.title('model mae')
        plt.ylabel('mae')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.show()
        # summarize history for loss
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'validation'], loc='upper left')
        plt.show()

        score_valid = self.model.evaluate(validation_matrix, validation_y,verbose=1)
        print("----------------------------------------------------")
        print("Validation score "+ variable_name + ": ", score_valid)
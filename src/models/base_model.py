import glob
import os 
from keras.utils import plot_model
from keras.models import Model
from keras.callbacks import ModelCheckpoint
import numpy as np
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
    
        self.model.fit(train_matrix, train_y, epochs=10, batch_size=128, verbose=1, validation_split=0.2, shuffle=True,callbacks=[checkpointer])

        #y_pred = model.predict(test_matrix)

        score_valid = self.model.evaluate(validation_matrix, validation_y,verbose=1)
        print("----------------------------------------------------")
        print("Validation score "+ variable_name + ": ", score_valid)
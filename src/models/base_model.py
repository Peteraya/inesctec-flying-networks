from keras.utils import plot_model
from keras.models import Model
import numpy as np
from abc import ABCMeta, abstractmethod

class BaseModel:
    @abstractmethod
    def __init__(self):
        pass

    def print_model(self, filename):
        plot_model(self.model, to_file = '../../DataSet'+filename)

    def run(self, train_matrix, train_y, validation_matrix, validation_y, variable_name):
    
        self.model.fit(train_matrix, train_y, epochs=20, batch_size=1, verbose=1)

        #y_pred = model.predict(test_matrix)

        score_valid = self.model.evaluate(validation_matrix, validation_y,verbose=1)
        print("----------------------------------------------------")
        print("Validation score "+ variable_name + ": ", score_valid)
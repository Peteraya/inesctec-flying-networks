from keras.utils import plot_model
from keras.models import Model
import numpy as np
from abc import ABCMeta, abstractmethod

class BaseModel:
    @abstractmethod
    def __init__(self):
        pass

    '''def build_model():
        #input layer
        visible = Input(shape=(2,10,10))

        conv1 = Conv2D(32, kernel_size=1, activation='relu')(visible)
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
        conv2 = Conv2D(16, kernel_size=1, activation='relu')(pool1)
        pool2 = MaxPooling2D(pool_size=(1, 1))(conv2)
        flat = Flatten()(pool2)
        hidden1 = Dense(10, activation='relu')(flat)
        hidden2 = Dense(10, activation='relu')(hidden1)

        #output layers
        output = Dense(1, activation='sigmoid')(hidden2)
        model = Model(inputs=visible, outputs=output)
    
        plot_model(model, to_file='../DataSet/model.png')
        #model.compile(optimizer = "adam", loss="mse", accuracy="rmse")
        return model'''

    def print_model(self, filename):
        plot_model(self.model, to_file = '../../DataSet'+filename)

    def run(self, train_matrix, train_y, validation_matrix, validation_y, variable_name):
    
        self.model.fit(train_matrix, train_y, epochs=2, batch_size=1, verbose=1)

        #y_pred = model.predict(test_matrix)

        score_valid = self.model.evaluate(validation_matrix, validation_y,verbose=1)
        print("----------------------------------------------------")
        print("Validation score "+ variable_name + ": ", score_valid)
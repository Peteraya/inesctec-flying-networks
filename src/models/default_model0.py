from keras.utils import plot_model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from models.base_model import *
from keras.optimizers import *

class DefaultModel(BaseModel):
    
    def __init__(self):
        #input layer
        visible = Input(shape=(2,10, 10))

        conv1 = Conv2D(32, kernel_size=1, data_format = "channels_first", activation='relu')(visible)
        pool1 = MaxPooling2D(pool_size=(2, 2), data_format = "channels_first")(conv1)
        conv2 = Conv2D(16, kernel_size=1, data_format = "channels_first", activation='relu')(pool1)
        pool2 = MaxPooling2D(pool_size=(2, 2), data_format = "channels_first")(conv2)
        flat = Flatten(data_format = "channels_first")(pool2)
        hidden1 = Dense(10, activation='sigmoid', kernel_initializer='normal')(flat)
        hidden2 = Dense(10, activation='sigmoid', kernel_initializer='normal')(hidden1)

        #output layers
        output = Dense(1, activation='relu', kernel_initializer='normal')(hidden2)
        model = Model(inputs=visible, outputs=output)
    
        
        #model.compile(optimizer = "adam", loss="mse", accuracy="rmse")
        self.model = model

        self.print_model( "default_model.png")
        rmsprop = RMSprop(lr=0.01)
        self.model.compile(optimizer = rmsprop, loss="mse", metrics=['mae'])

'''
Results (20 Epochs):
Train throughput: loss: 0.5273 - mean_absolute_error: 0.5324
Validation score throughput:  [1.961517906486988, 1.0444690936803818]

Settins:
#Global Variables
SCENARIO_ROWS = 10
SCENARIO_COLUMNS = 10
SCENARIO_TOPOLOGIES_NO = 200
SCENARIOS_NO = 10
TOPOLOGIES_TRAINING = 128
TOPOLOGIES_VALIDATION = 32
TOPOLOGIES_TESTING = 40
SCENARIOS_TRAINING = [1, 2, 4, 6, 7, 10]
SCENARIOS_VALIDATION = [5, 9]
SCENARIOS_TEST = [3, 8]
DIVISION_BY_TOPOLOGIES = 0
DISTANCE_ENCODING = 1
NORMALIZE_DATA = 1
USE_TRANSFORMATIONS = 1
'''
import numpy as np 
np.random.seed(1337)

from keras.utils import plot_model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from models.base_model import *
from keras.optimizers import *
from keras.layers import LeakyReLU


class DefaultModel(BaseModel):
    
    def __init__(self):
        #input layer
        visible = Input(shape=(2,10, 10))

        conv1 = Conv2D(32, kernel_size=3, data_format = "channels_first", activation='relu')(visible)
        #pool1 = MaxPooling2D(pool_size=(2, 2), data_format = "channels_first")(conv1)
        conv2 = Conv2D(64, kernel_size=3, data_format = "channels_first", activation='relu')(conv1)
        pool2 = MaxPooling2D(pool_size=(2, 2), data_format = "channels_first")(conv2)
        flat = Flatten(data_format = "channels_first")(pool2)
        hidden1 = Dense(10, activation='relu', kernel_initializer='normal')(flat)
        hidden2 = Dense(10, activation='relu', kernel_initializer='normal')(hidden1)

        #output layers
        pre_output = Dense(1, activation='linear', kernel_initializer='normal')(hidden2)
        output = LeakyReLU()(pre_output)
        model = Model(inputs=visible, outputs=output)
    
        
        #model.compile(optimizer = "adam", loss="mse", accuracy="rmse")
        self.model = model

        self.print_model( "default_model.png")
        rmsprop = RMSprop(lr=0.01)
        self.model.compile(optimizer = rmsprop, loss="mse", metrics=['mae'])
        self.model.summary()
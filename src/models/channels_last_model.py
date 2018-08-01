"""
This module defines the class ChannelsLastModel
"""
import numpy as np
np.random.seed(1337)

from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
import keras.optimizers
from keras.layers import LeakyReLU
from keras.models import Model
import models.base_model


class ChannelsLastModel(models.base_model.BaseModel):
    """
    Class that represents a ML model where the channels of image to be given as input to the CNN come last
    """
    
    def __init__(self, variable_name):
        """
        Constructor of the class

        Args:
            variable_name: Name of the variable which this model tries to compute
        """
        self.variable_name = variable_name
        #input layer
        visible = Input(shape=(10,10, 2))

        conv1 = Conv2D(32, kernel_size=3, activation='relu')(visible)
        conv2 = Conv2D(64, kernel_size=3, activation='relu')(conv1)
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
        flat = Flatten(data_format = "channels_first")(pool2)
        hidden1 = Dense(10, activation='relu', kernel_initializer='normal')(flat)
        hidden2 = Dense(10, activation='relu', kernel_initializer='normal')(hidden1)

        #output layers
        pre_output = Dense(1, activation='linear', kernel_initializer='normal')(hidden2)
        output = LeakyReLU()(pre_output)
        model = Model(inputs=visible, outputs=output)
            
        self.model = model

        self.print_model( "default_model.png")
        adam_opt = keras.optimizers.Adam(lr=0.01)
        self.model.compile(optimizer = adam_opt, loss="mse", metrics=['mae', models.base_model.mean_absolute_percentage_error])
        self.model.summary()
"""
This module defines the class DefaultModel
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




class DefaultModel(models.base_model.BaseModel):
    """
    This class represents the default model used in our program.
    It consists of a convolutional neural network with convolutional, pooling and dense layers.
    """
    
    def __init__(self, learning_rate, variable_name, extra_layer=False):
        """
        Constructor of the class DefaultModel.

        Args:
            learning_rate: Learning Rate used by the optimizer of this model.
            variable_name: Name of the variable this model is trying to predict.
            extra_layer: If true, an extra layer consisting of a convolutional layer will be added.
        """
        self.variable_name = variable_name
        #input layer
        visible = Input(shape=(2,10, 10))
        model_printing_name= "default_model.png"

        conv1 = Conv2D(32, kernel_size=3, data_format = "channels_first", activation='relu')(visible)
        conv2 = Conv2D(64, kernel_size=3, data_format = "channels_first", activation='relu')(conv1)
        if(extra_layer):
            conv3 = Conv2D(64, kernel_size=3, data_format = "channels_first", activation='relu')(conv2)
            pool2 = MaxPooling2D(pool_size=(2, 2), data_format = "channels_first")(conv3)
            model_printing_name = "extra_layer_model.png"
        else:
            pool2 = MaxPooling2D(pool_size=(2, 2), data_format = "channels_first")(conv2)
        flat = Flatten(data_format = "channels_first")(pool2)
        hidden1 = Dense(10, activation='relu', kernel_initializer='normal')(flat)
        hidden2 = Dense(10, activation='relu', kernel_initializer='normal')(hidden1)

        #output layers
        pre_output = Dense(1, activation='linear', kernel_initializer='normal')(hidden2)
        output = LeakyReLU()(pre_output)
        model = Model(inputs=visible, outputs=output)
    
        
        self.model = model

        
        self.print_model(model_printing_name)
        adam_opt = keras.optimizers.Adam(lr=learning_rate)
        self.model.compile(optimizer = adam_opt, loss="mse", metrics=['mae', models.base_model.mean_absolute_percentage_error])
        self.model.summary()
        
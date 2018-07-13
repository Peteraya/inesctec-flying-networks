from keras.utils import plot_model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from models.base_model import *

class DefaultModel(BaseModel):
    
    def __init__(self):
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
    
        
        #model.compile(optimizer = "adam", loss="mse", accuracy="rmse")
        self.model = model

        self.print_model( "default_model.png")

        self.model.compile(optimizer = "adam", loss="mse", metrics=['mae'])
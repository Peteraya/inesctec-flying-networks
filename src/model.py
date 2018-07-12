from keras.utils import plot_model
from keras.models import Model
from keras.layers import Input
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D



def build_model():
    #input layer
    visible = Input(shape=(10,10,3))

    conv1 = Conv2D(32, kernel_size=3, activation='relu')(visible)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    conv2 = Conv2D(16, kernel_size=3, activation='relu')(pool1)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    flat = Flatten()(pool2)
    hidden1 = Dense(10, activation='relu')(flat)
    hidden2 = Dense(10, activation='relu')(hidden1)

    #output layers
    output = Dense(1, activation='sigmoid')(hidden2)
    model = Model(inputs=visible, outputs=[output])
    print(model.summary())
    plot_model(model, to_file='../DataSet/model.png')
    model.compile(optimizer = "adam", loss="mse", accuracy="rmse")
    return model



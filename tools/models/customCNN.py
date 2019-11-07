import matplotlib.pyplot as plt
import numpy as np
import os

from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D
from keras.utils.np_utils import to_categorical
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator
from keras import backend as K

trainImageDataGen = ImageDataGenerator(horizontal_flip=False)
trainGenerator = trainImageDataGen.flow_from_directory(
    '../../data/train',
    target_size=(400, 400),
    batch_size=64,
    class_mode='categorical')

validImageDataGen = ImageDataGenerator()
validGenerator = validImageDataGen.flow_from_directory(
    '../../data/valid',
    target_size=(400, 400),
    batch_size=64,
    class_mode='categorical')



model = Sequential()
model.add(Conv2D(64, kernel_size=(3, 3),padding = "valid", strides = 2, input_shape=(400, 400, 3),
                 activation= 'relu', kernel_initializer='glorot_uniform'))
model.add(MaxPool2D(pool_size = (2, 2)))

model.add(Conv2D(32, kernel_size=(3, 3), padding = "valid", strides = 2,
                 activation ='relu', kernel_initializer = 'glorot_uniform'))
model.add(MaxPool2D(pool_size = (2, 2)))

model.add(Conv2D(16, kernel_size=(3, 3), padding = "valid", strides = 2,
                 activation ='relu', kernel_initializer = 'glorot_uniform'))
model.add(MaxPool2D(pool_size = (2, 2)))

model.add(Flatten())
model.add(Dense(32, activation='relu'))
model.add(Dense(3, activation='softmax'))
model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=Adam(lr=1e-4),
              metrics=['acc'])

history = model.fit_generator(
    trainGenerator,
    epochs=5,
    validation_data=validGenerator,
    verbose=1)

model.save("../../app/resources/models/Xception.h5")

print(history.history.keys())
plt.plot(history.history['acc'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

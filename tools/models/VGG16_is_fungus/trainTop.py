import matplotlib.pyplot as plt
import numpy as np
from keras import regularizers

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils.np_utils import to_categorical
from keras.optimizers import Adam
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.decomposition import PCA
from keras.callbacks.callbacks import ModelCheckpoint

train_data = np.loadtxt('vgg16_train.csv', delimiter=",")
s = np.arange(train_data.shape[0])
np.random.shuffle(s)

train_data = train_data[s]
train_X = train_data[:, :-1]


validation_data = np.loadtxt('vgg16_validation.csv', delimiter=",")
validation_X = validation_data[:, :-1]

# pca = PCA(n_components=50)
# pca = pca.fit(train_X)
# train_X = pca.transform(train_X)
# validation_X = pca.transform(validation_data[:, :-1])


# tree = RandomForestClassifier(n_estimators=1000)
# tree = tree.fit(train_X, train_data[:, -1])
# print(tree.score(train_X, train_data[:, -1]))
# print(tree.score(validation_X, validation_data[:, -1]))
# exit()
model = Sequential()

# model.add(Dense(128, activation='relu', kernel_initializer='he_uniform', input_shape=(512,), kernel_regularizer=regularizers.l2(0.1), bias_regularizer=regularizers.l2(0.1)))
# model.add(Dropout(0.5))
# model.add(Dense(64, activation='relu', kernel_initializer='he_uniform', kernel_regularizer=regularizers.l2(0.1), bias_regularizer=regularizers.l2(0.1)))


model.add(Dense(1, activation='sigmoid', input_shape=(512,)))
model.summary()

model.compile(loss='binary_crossentropy',
              optimizer=Adam(lr=500e-6, decay=0.001),
              metrics=['acc'])

history = model.fit(
    x=train_X,
    y=train_data[:, -1],
    epochs=200,
    batch_size=1024,
    validation_data=(validation_X, validation_data[:, -1]),
    callbacks=[ModelCheckpoint("vgg19_is_fungus_{val_acc:.4f}_{val_loss:.4f}_{epoch:02d}.h5", save_best_only=True, monitor='acc',
                               verbose=0, mode='auto', period=1)],
    verbose=2)

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
# plt.title('Dokładność modelu')
plt.ylabel('Dokładność modelu')
plt.xlabel('Epoka')
plt.legend(['Zbiór trenujący', 'Zbiór walidujący'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
# plt.title('model loss')
plt.ylabel('Funkcja kosztu')
plt.xlabel('Epoka')
plt.legend(['Zbiór trenujący', 'Zbiór walidujący'], loc='upper left')
plt.show()

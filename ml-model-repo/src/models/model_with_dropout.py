import tensorflow as tf
import keras
from keras import layers


def build_and_compile_cnn_model_with_dropout():
   print ("Training CNN model with dropout")
   model = keras.Sequential()
   model.add(layers.Input(shape=(28, 28, 1), name='image _bytes'))
   model.add(layers.Conv2D(32, (3, 3), activation='relu'))
   model.add(layers.MaxPooling2D((2, 2)))
   model.add(layers.Conv2D(64, (3, 3), activation='relu'))
   model.add(layers.MaxPooling2D((2, 2)))
   model.add(layers.Dropout (0.5) )
   model.add(layers.Conv2D(64, (3, 3), activation='relu'))
   model.add(layers.Flatten())
   model.add(layers.Dense(64, activation='relu'))
   model.add(layers.Dense(10, activation='softmax'))
   model.summary()
   model.compile(optimizer='adam',loss='sparse_categorical_crossentropy', metrics=['accuracy'])

from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D, BatchNormalization
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.preprocessing import image

import numpy as np
import os

# image size
img_width, img_height = 379,288
# train and test sample sizes
train_samples = 665
test_samples = 98
# set weights
epochs = 125
batch_size = 20
# Directories of train and test data
train_dir ='cut_image/Train'
test_dir = 'cut_image/Test'

# data image augmentation to create more variation of XRD patterns
train_data = ImageDataGenerator(rescale=1. / 255,
                                shear_range=0.2,
                                zoom_range=0.2,
                                horizontal_flip=True)

# only resize for test data
test_data = ImageDataGenerator(rescale=1. / 255)

# import train data consisting of 'binary' or  2 classifications (BCC or FCC) 
def train_gen():
    result_train_gen=train_data.flow_from_directory(train_dir, target_size=(img_width, img_height),
                                           batch_size=batch_size,
                                           class_mode='binary',)
    return result_train_gen

# import test data consisting of 'binary' or  2 classifications (BCC or FCC) 
def test_gen():
    result_test_gen= test_data.flow_from_directory(test_dir, target_size=(img_width, img_height),
                                         batch_size=batch_size,
                                         class_mode='binary')
    return result_test_gen

# build CNN model
def CNN_model():
    model = Sequential()
    # extract features by iterating across image
    model.add(Conv2D(32, (3, 3), activation='relu',
                     input_shape=(img_width, img_height, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(64, (3, 3), activation='relu',
                 input_shape=(img_width, img_height, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(96, (3, 3), activation='relu', padding='valid',
                     input_shape=(img_width, img_height, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.summary()

    return model



def train_model():
    model = Sequential()
    # extract features by iterating across image
    model.add(Conv2D(32, (3, 3), activation='relu',
                     input_shape=(img_width, img_height, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(64, (3, 3), activation='relu',
                 input_shape=(img_width, img_height, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Conv2D(96, (3, 3), activation='relu', padding='valid',
                     input_shape=(img_width, img_height, 3)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.2))

    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.summary()

    
    # compile model
    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    cs_classification = model.fit_generator(train_gen,
                        steps_per_epoch=train_samples // batch_size,
                        epochs=epochs,
                        validation_data=test_gen,
                        validation_steps=test_samples // batch_size)
    return cs_classification


# plot model data
def plot_data():
    x = np.arange(0, epochs)
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    fig.subplots_adjust(wspace=0.2)
    fig.suptitle("CNN Model", y=.98, fontsize=17)
    ax[0].set_xlabel("Epoch Number")
    ax[1].set_xlabel("Epoch Number")
    ax[0].set_ylabel("Loss")
    ax[1].set_ylabel("Accuracy")
    ax[0].plot(x, cs_classification.history["loss"], label="Training Loss")
    ax[0].plot(x, cs_classification.history["val_loss"], label="Validation Loss")
    ax[1].plot(x, cs_classification.history["acc"], label="Training Accuracy")
    ax[1].plot(x, cs_classification.history["val_acc"], label="Validation Accuracy")
    ax[0].set_title('Training/Validation Loss')
    ax[1].set_title('Training/Validation Accuracy')
    ax[0].legend(loc="upper right")
    ax[1].legend(loc="lower right")
    print('loss: %.2f' %(np.amin(cs_classification.history["loss"])))
    print('Validation loss: %.2f' %(np.amin(cs_classification.history["val_loss"])))
    print('Accuracy: %.2f' %(np.amax(cs_classification.history["acc"])))
    print('Validation Accuracy: %.2f' %(np.amax(cs_classification.history["val_acc"])))
    print('Mean Loss: %.2f' %(np.mean(cs_classification.history["loss"])))
    print('Mean Validation Loss: %.2f' %(np.mean(cs_classification.history["val_loss"])))
    print('Mean Accuracy: %.2f' %(np.mean(cs_classification.history["acc"])))
    print('Mean Validation Accuracy: %.2f' %(np.mean(cs_classification.history["val_acc"])))
    
    return


    
    
    

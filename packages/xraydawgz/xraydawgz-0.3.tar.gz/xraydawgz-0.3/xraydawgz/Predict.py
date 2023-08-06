from tensorflow import keras
from keras.preprocessing import image

import os
import numpy as np
import h5py


class Predict(object):
    """
    This class contains the prediction fucntion for classifying crystal
    structures.
    """
    def crystal_structure(path_to_image):
        """
        This function takes the input XRD pattern/image and runs it through the
        CNN model to predict the crystal structure.
        """
        h5file = h5py.File('crystal_structure_classifier.h5', 'r')
        cnn_model = keras.models.load_model(h5file)
        for file in os.listdir(path_to_image):
            predict_img = image.load_img(path_to_image+file,
                                         target_size=(379, 288))
            predict_img = image.img_to_array(predict_img)
            predict_img = np.expand_dims(predict_img, axis=0)
            result = cnn_model.predict(predict_img)
            if np.round(result, 0) == 0:
                print(str(file) + ' is BCC!')
            else:
                print(str(file) + ' is FCC!')

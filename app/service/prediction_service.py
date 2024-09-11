from tensorflow.keras.models import load_model
import numpy as np
import cv2
from sklearn.preprocessing import MinMaxScaler
from patchify import patchify

model = load_model('model/tea_plant_segment.hdf5')

def get_predicted_mask(normalized_patched_images):
    prediction = model.predict(normalized_patched_images)
    prediction = np.squeeze(prediction)
    return prediction
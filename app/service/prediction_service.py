import numpy as np
from patchify import unpatchify

from lib.smooth_tiled_predictions import predict_img_with_smooth_windowing
    
def get_predicted_mask_with_smooth_windowing(self, input_img, image_patch_size):
    predictions_smooth = predict_img_with_smooth_windowing(
        input_img,
        window_size=image_patch_size,
        subdivisions=2,
        nb_classes=1,
        pred_func=(lambda img_batch_subdiv: model.predict((img_batch_subdiv)))
    )

    final_prediction = (predictions_smooth > 0.1).astype(np.uint8)
    return final_prediction

def get_predicted_mask_with_unpatchify(input_img, patched_images):
    print("start prediction function....")

    import tensorflow as tf
    from tensorflow.keras.models import load_model
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.experimental.set_memory_growth(gpus[0], True)
        except RuntimeError as e:
            print(f"Error setting memory growth: {e}")
    print("Num GPUs available: ", len(gpus))
    model = load_model('model/tea_plant_segment.hdf5', compile=False)
    prediction = model.predict(input_img)
    expected_shape = (patched_images.shape[0], patched_images.shape[1], patched_images.shape[2], patched_images.shape[3],patched_images.shape[4], 1)

    patched_prediction = np.reshape(prediction, expected_shape)

    unpatched_prediction = unpatchify(patched_prediction, (patched_images.shape[0] * 256, patched_images.shape[1] * 256, 1))
    print("finish prediction function....")
    return unpatched_prediction
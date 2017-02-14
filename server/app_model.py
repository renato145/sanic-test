import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
from time import time
from PIL import Image as pil_image
from keras.preprocessing import image
from keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions

IMG_SIZE = (299, 299)


def load_model():
	t0 = time()
	model = InceptionV3()
	print('Model loaded (%.2fs).' % (time() - t0))

	return model


def get_pred(src, model, file_type, img_size=IMG_SIZE):
    if file_type == 'file':
    	x = np.asarray(bytearray(src), dtype="uint8")
    	x = cv2.imdecode(x, cv2.IMREAD_COLOR)
    	x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
    elif file_type == 'url':
        x = imutils.url_to_image(src)
        x = cv2.cvtColor(x, cv2.COLOR_BGR2RGB)
    elif file_type == 'path':
        x = plt.imread(src)
    else:
    	return 'Invalid file type.'
                
    x = cv2.resize(x, img_size)
    x = image.img_to_array(x)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    y = model.predict(x)
    preds = decode_predictions(y)
    preds = {l:float(p) for _, l, p in preds[0]}

    return preds

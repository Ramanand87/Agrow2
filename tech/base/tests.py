from django.test import TestCase
import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import numpy as np
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
import matplotlib.pyplot as plt
from keras import Sequential
from keras.layers import Dense,Conv2D,MaxPooling2D,Flatten,BatchNormalization,Dropout
from PIL import Image
# Create your tests here.
new_model = tf.keras.models.load_model('C:\\Users\\Dushyant\\Desktop\\padh le saale\\hack2\\AgriTech\\tech\\base\\soil.h5', custom_objects={'KerasLayer':hub.KerasLayer})
custom_image = Image.open("c:\\Users\\Dushyant\\Downloads\\1.jpeg")  # Replace "path/to/your/image.jpg" with the path to your image file
custom_image = custom_image.resize((224, 224))  # Resize the image to match the input size of your model
custom_image_array = np.array(custom_image) / 255.0  # Normalize the image pixel values

# Display the custom image
plt.imshow(custom_image)
plt.axis('off')
plt.show()

# Expand the custom image to (1, 224, 224, 3) before predicting the label
custom_image_array = np.expand_dims(custom_image_array, axis=0)

# Predict the label for the custom image
prediction_scores = new_model.predict(custom_image_array)
predicted_index = np.argmax(prediction_scores)
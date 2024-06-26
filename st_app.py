# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14k1-65syE6s0aUNj44IVGOXEoK553c8z
"""

import streamlit as st
import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

# Load the model with caching
@st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model('final_model_compressed.hdf5')  # Correct path to your model
    return model

model = load_model()

# Set up the page layout
st.write("""
# Cat and Dog Image Classifier
Upload an image of a cat or dog and the model will predict which category it belongs to.
""")

# File uploader widget
file = st.file_uploader("Choose an image...", type=["jpg", "png"])

# Function to preprocess and predict the image
def import_and_predict(image_data, model):
    # Resize and rescale the image
    size = (150, 150)  # Same as during training
    image = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)  # Updated from Image.ANTIALIAS
    img = np.asarray(image)
    img_rescaled = img / 255.0  # Rescale as in training
    img_reshape = img_rescaled[np.newaxis, ...]  # Add batch dimension
    prediction = model.predict(img_reshape)
    return prediction

# Display the uploaded image and run prediction
if file is None:
    st.text("Please upload an image file.")
else:
    image = Image.open(file)
    st.image(image, use_column_width=True)
    prediction = import_and_predict(image, model)
    class_names = ['Dog', 'Cat']  # Ensure order matches training
    result = "This image most likely belongs to a {}.".format(class_names[int(prediction[0][0] > 0.5)])
    st.success(result)

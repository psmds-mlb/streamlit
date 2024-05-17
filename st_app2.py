# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14k1-65syE6s0aUNj44IVGOXEoK553c8z
"""

import streamlit as st

# Configure the page before anything else
st.set_page_config(page_title="Cat & Dog Classifier", layout="wide")

import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np

# Color themes for aesthetics
darkBlueColor = "#003366"  # Dark blue
backgroundColor = "#E0FFFF"  # Light Cyan, complementary with dark blue
secondaryBackgroundColor = "#F0FFFF"  # Azure, slightly darker shade of Light Cyan
textColor = "#262730"  # Almost black
font = "sans serif"

st.markdown(f"""
<style>
    html, body, .reportview-container .main {{
        background-color: {backgroundColor} !important;
    }}
    .sidebar .sidebar-content {{
        background-color: {secondaryBackgroundColor} !important;
    }}
    h1, h2 {{
        color: {darkBlueColor};
    }}
    .stButton > button {{
        border: 2px solid {darkBlueColor};
        border-radius: 10px;
        font-size: 16px;
    }}
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: {secondaryBackgroundColor};
        color: {textColor};
        text-align: center;
        padding: 10px;
        font-size: 18px;  /* Increased font size */
    }}
</style>
""", unsafe_allow_html=True)


# Load the model with caching
@st.cache(allow_output_mutation=True)
def load_model():
    model = tf.keras.models.load_model('final_model_compressed.hdf5')  # Correct path to your model
    return model

model = load_model()

# Display course name and app title
st.markdown("""
## PSMDSSC 104-PSMDS001 - Advanced Data Science
""")
st.title("Cat and Dog Image Classifier 🐱🐶")
st.markdown("""
Upload an image of a cat or dog, and the model will predict which category it belongs to.
Try to upload a clear image for the best results!
""")

# File uploader widget with clearer instructions
file = st.file_uploader("Choose an image file (JPEG or PNG format)", type=["jpg", "png"])

# Function to preprocess and predict the image
def import_and_predict(image_data, model):
    size = (150, 150)  # Target size as per model's training
    image = ImageOps.fit(image_data, size, Image.Resampling.LANCZOS)  # Best resampling method
    img = np.asarray(image)
    img_rescaled = img / 255.0  # Normalize pixel values as during model training
    img_reshape = img_rescaled[np.newaxis, ...]  # Add batch dimension
    prediction = model.predict(img_reshape)
    return prediction

# Display the uploaded image and run prediction
if file is None:
    st.warning("Please upload an image file.")  # More contextual feedback for no file
else:
    image = Image.open(file)
    st.image(image, use_column_width=True, caption="Uploaded Image")
    prediction = import_and_predict(image, model)
    class_names = ['Dog', 'Cat']  # Maintain order as per training
    result = class_names[int(prediction[0][0] > 0.5)]
    st.success(f"This image most likely belongs to a {result}.")  # Formatted result text

# Footer
st.markdown('<div class="footer">Submitted by: BELEN, Marvin L.</div>', unsafe_allow_html=True)

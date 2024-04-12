import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="Similarity Search", page_icon="📈")

st.markdown("# Similarity Search")
st.sidebar.header("Similarity Search")
st.write(
    """This page allows you to search for similar images within your data. 
    Remove duplicates to improve the quality of your dataset."""
)
st.write("""First you need to enter the local path to your dataset. \n
    |-my_images
    |--image_1.png
    |--image_2.jpg
    |--image_3.jpeg""")

with st.form("s3_path"):
    local_image_path = st.text_input("Enter a valid local path here:")
    submit_button_image_path = st.form_submit_button("Import Images")

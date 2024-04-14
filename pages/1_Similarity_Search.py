import logging

import streamlit as st
from utils.similarity_search.dataloader import DataLoader, filter_images_based_on_threshold, find_top_k_image_pairs
from utils.similarity_search.model import SimilarImages

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

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

col1, col2 = st.columns(2)

if "loaded_images" not in st.session_state:
    st.session_state.loaded_images = False

if "similar_images" not in st.session_state:
    st.session_state.similar_images = None

with st.form("s3_path"):
    local_image_path = st.text_input("Enter a valid local path here:")
    submit_button_image_path = st.form_submit_button("Import Images")

similarity_threshold = st.sidebar.slider("Similarity Threshold", min_value=0.0, max_value=1.0, step=0.01, key="similarity_threshold")
top_k_slider = st.sidebar.slider("Top-k Similar Images", min_value=5, max_value=1, step=1, key="top_k_slider")

if submit_button_image_path:
    st.session_state.loaded_images = True
    st.session_state.similar_images = DataLoader(image_path=local_image_path, similarity_threshold=similarity_threshold).get_similar_images()

if st.session_state.similar_images is not None:
    filtered_images: SimilarImages = filter_images_based_on_threshold(st.session_state.similar_images, similarity_threshold)
    top_k_image_pairs: SimilarImages = find_top_k_image_pairs(filtered_images, top_k_slider)
    logger.info(f"Number of filtered ImagePairs: {len(filtered_images.similar_images)}")
    for similar_image in top_k_image_pairs.similar_images:
        with col1:
            st.image(similar_image.image1_path)
        with col2:
            st.image(similar_image.image2_path)

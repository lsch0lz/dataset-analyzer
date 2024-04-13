import streamlit as st

from utils.similarity_search.dataloader import DataLoader
from utils.similarity_search.model import SimilarImages

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

if "similarity_threshold" not in st.session_state:
    st.session_state.similarity_threshold = 0

with st.form("s3_path"):
    local_image_path = st.text_input("Enter a valid local path here:")
    submit_button_image_path = st.form_submit_button("Import Images")

similarity_threshold = st.sidebar.slider("Similarity Threshold", min_value=0.0, max_value=1.0, step=0.1, key="similarity_threshold")

if submit_button_image_path:
    st.session_state.loaded_images = True

# Display images if they are loaded
if st.session_state.loaded_images:
    similar_images: SimilarImages = DataLoader(image_path=local_image_path, similarity_threshold=similarity_threshold).get_similar_images()
    for similar_image in similar_images.similar_images:
        with col1:
            st.image(similar_image.image1_path)
        with col2:
            st.image(similar_image.image2_path)

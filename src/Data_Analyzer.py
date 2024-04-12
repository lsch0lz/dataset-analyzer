import streamlit as st

st.set_page_config(
    page_title="Data Analyzer",
    page_icon="👋",
)

st.write("# Welcome to Data Analyzer! 👋")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    The Data Analyzer is a small tool to enhance the quality of your image dataset. 
    You can find image duplicates with the **Similarity Search** Page, find outliers with the **Outlier Analysis** Page or 
    check the class balance on various features with the **Class Balance** Page.
    
    Feel free to improve the Data Analyzer by submitting a PR on the official [Repository](https://github.com/lsch0lz/dataset-analyzer) 
"""
)

import streamlit as st
from PIL import Image



st.title("Gel Entry Form")

st.header("PCR Date")
gel_date = st.date_input("Gel Date",value="today")


st.header("Samples")
with st.container():
    for label in "ABCDEFGH":
        st.text_input(f"{label}")

st.header("Top Row")
top_row = st.selectbox("Primer Set",("28SVX","HCO","m13","None"))

st.header("Bottom Row")
bottom_row = st.selectbox("Primer Set",("28SVX","HCO","m13","None"),index=1)

st.header("Gel Image")
gel_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg","tif"])


if gel_image is not None:
    # Open the uploaded file as an image
    image = Image.open(gel_image)
    
    # Display the image
    st.image(image, caption="Uploaded Image", use_column_width=True)
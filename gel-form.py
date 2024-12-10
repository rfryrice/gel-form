import streamlit as st
import pandas as pd
from PIL import Image

st.title("Gel Entry Form")

with st.form("gel"):
    st.header("PCR Date")
    gel_date = st.date_input("Gel Date",value="today")


    st.header("Samples")
    with st.container():
        df = pd.DataFrame(
            [
                {"sample": "A", "lane": 2, "label":" ", "is_band": True},
                {"sample": "B", "lane": 3, "label":" ", "is_band": False},
                {"sample": "C", "lane": 4, "label":" ", "is_band": True},
                {"sample": "D", "lane": 5, "label":" ", "is_band": True},
                {"sample": "E", "lane": 6, "label":" ", "is_band": False},
                {"sample": "F", "lane": 7, "label":" ", "is_band": True},
                {"sample": "G", "lane": 8, "label":" ", "is_band": True},
                {"sample": "H", "lane": 9, "label":" ", "is_band": False},
            ]
        )
        edited_df = st.data_editor(
            df,
            column_config={
                "sample": "Sample",
                "lane": st.column_config.NumberColumn(
                    "Lane",
                    help="Change if loaded differently",
                    min_value=1,
                    max_value=14,
                    step=1,
                ),
                "label":st.column_config.Column(
                    "Label",
                    help="Enter the label on tube verbatim",
                    width="large",),
                "is_band": "Band?",
            },
            disabled=["sample"],
            hide_index=True,
        )


    st.header("Top Row")
    gel_top = st.selectbox("Primer Set",("28SVX","HCO","m13","None"))

    st.header("Bottom Row")
    gel_bottom = st.selectbox("Primer Set",("28SVX","HCO","m13","None"),index=1)

    st.header("Gel Image")
    gel_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg","tif"])


    if gel_image is not None:
        # Open the uploaded file as an image
        image = Image.open(gel_image)
        
        # Display the image
        st.image(image, caption="Uploaded Image", use_column_width=True)

    complete = st.form_submit_button()

if complete:
    pass

#TODO: Process entered data after submit
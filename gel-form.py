import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from PIL import Image
import numpy as np

conn = st.connection("gsheets", type=GSheetsConnection)

st.title("Gel Entry Form")

st.header("Gel Image")
gel_image = st.file_uploader("Upload an image", type=["tif","png", "jpg",])

if gel_image is not None:
    # Open the uploaded file as an image
    image = Image.open(gel_image,formats=["tiff","png", "jpg"])

    if image.format == "TIFF":
        #PIL image conversion sucks ass
        #I to L conversion
        img_arr = np.uint8(np.array(image) / 256)
        st.image(img_arr, caption="Uploaded Image")
    else:
        st.image(image, caption="Uploaded Image")

with st.form("gel"):
    st.header("PCR Date")
    gel_date = st.date_input("Gel Date",value="today",label_visibility="collapsed")


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
                "is_band":"Band",
            },
            disabled=["sample"],
            hide_index=True,
            use_container_width=True
        )


    st.header("Primer set")
    gel_primer = st.selectbox("Primer Set",("28SVX","HCO","m13"),label_visibility="collapsed")

    complete = st.form_submit_button()

if complete:
    st.write("Added the following data to the spreadsheet")
    push_df = edited_df.copy()
    push_df['primer'] = gel_primer
    push_df['date'] = gel_date

    col_order = ['date','sample','lane','label','primer','is_band']
    push_df = push_df[col_order]

    with st.container():
        st.dataframe(push_df,use_container_width=True)

    
    # Read in spreadsheet
    sheet_df = conn.read()
    # Combine form and spreadsheet
    df_combined = pd.concat([sheet_df,push_df], ignore_index=True)

    conn.update(data=df_combined)

    st.cache_data.clear()
    #st.rerun()
    

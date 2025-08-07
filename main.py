
import streamlit as st
import pandas as pd 
import numpy as np
from PIL import Image


st.set_page_config ( page_title="data",
    page_icon="🎯",
    layout= "wide")
    

with st.sidebar:
    st.title(" options ")
    selected_page=st.radio("choose an option ",
       ["📂 form","📔csv uploader","🖼️image gallery"])
    index=0


if selected_page=="📂 form":
    st.header("User Information Form")
    with st.form("user_form"):
        name=st.text_input("enter your name:")
        age=st.number_input("enter your age")
        feedback=st.text_input("your feedback:")
        gender=st.radio("Gender:",["male","female"])
        workday=st.slider("How many days do you work per week? ",0,7,5)
        agree=st.checkbox("I accept the terms and conditions")
        submitted = st.form_submit_button("submit")
        if submitted:
            if agree :
                st.success("form submitted successfuly")
                st.write("Name:",name)
                st.write("Age:",age)
                st.write("Gender:",gender)
                st.write("active days per week",workday)
                st.write("Feedback:",feedback)
                st.write("you have accepted the Terms and conditions")
            else:
                st.error("you must agree to the terms and conditions")

if selected_page=="📔csv uploader":
    st.header("CSV uploader and interactive table")
    max_size=200
    uploaded_file=st.file_uploader(
        label="upload csv",
        type=["csv"],
        help="limit 200 MB per file.csv",
        label_visibility="visible")
    
    @st.cache_data
    def load_csv(file):
       return pd.read_csv(file)
    if uploaded_file is not None:
        file_mb=len(uploaded_file.getvalue())/(1024*1024)
        if file_mb>max_size:
            st.error("your file size is over 200 mb ")
        else:
           st.success("your file uploaded successfuly ")
           df = load_csv(uploaded_file)
           rows_per_page = 10
           total_pages = (len(df) - 1) // rows_per_page + 1
        
           st.header("Data Table")
           page_num=st.slider(
           label="page number ",
           min_value=1,
           max_value=total_pages,
           value=1,step=1 

            )
           start_idx = (page_num - 1) * rows_per_page
           end_idx = start_idx + rows_per_page
          
           displayed_df = df.iloc[start_idx:end_idx]



           st.markdown("### 🔽 Sort by column")
           selected_column=st.selectbox("Base columns",df.select_dtypes(include=['number']).columns)
        
           displayed_df = displayed_df.sort_values(by=selected_column)

           sorted_df=df.sort_values(by=selected_column,ascending=True)

           max_value=st.number_input(f"Only show rows where {selected_column} ≤ value:",min_value=0.0)
           if max_value>0:
                  filtered_df = displayed_df[displayed_df[selected_column] <= max_value]
           else:
              filtered_df = displayed_df
             
           st.dataframe(filtered_df, use_container_width=True)
          
               


    else:
         st.info("click browse button to upload your file")




if selected_page=="🖼️image gallery":
        
        max_size=200*1024*1024
        st.header("image gallery with batch upload")
        uploaded_files=st.file_uploader(
        label="upload images(JPG, JPEG, PNG)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        help="Max size per file: 200MB",
        label_visibility="visible")


        if uploaded_files:
          for uploaded_file in uploaded_files:
            file_size = len(uploaded_file.getvalue())
            if file_size > max_size:
              st.error(" File is larger than 200MB. ")
            else:
              st.success(f"✅ File '{uploaded_file.name}' uploaded successfully.")

            
            image = Image.open(uploaded_file)
            st.image(image, caption=uploaded_file.name, use_column_width=True)
else:
    st.info("📂 Click 'Browse files' to upload images.")




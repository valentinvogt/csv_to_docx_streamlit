import pandas as pd
import streamlit as st
from parse_docx import parse_docx, adapt_data

#importing required libraries

import streamlit as st

@st.cache_data
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

file = st.file_uploader("Please choose a file")

if file is not None:
   status, data = parse_docx(file)
   if status != "OK":
      st.error(status)
      st.stop()

   csv = convert_df(adapt_data(data))

   st.success("CSV file successfully created!")

   st.download_button(
      "Press to Download",
      csv,
      f"{file.name[:-5]}.csv",
      "text/csv",
      key='download-csv'
   )

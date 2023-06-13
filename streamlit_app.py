from collections import namedtuple
import altair as alt
from parse_docx import docx_to_csv
import pandas as pd
import streamlit as st

#importing required libraries

import streamlit as st

from io import StringIO 

@st.experimental_memo
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

file = st.file_uploader("Please choose a file")

if file is not None:

   status, df = docx_to_csv(file)
   if status != "OK":
      st.error(status)
      st.stop()

   csv = convert_df(df)

   st.success("CSV file successfully created!")

   st.download_button(
      "Press to Download",
      csv,
      "file.csv",
      "text/csv",
      key='download-csv'
   )

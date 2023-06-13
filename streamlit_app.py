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

#adding a file uploader

file = st.file_uploader("Please choose a file")

if file is not None:
   #Can be used wherever a "file-like" object is accepted:
   status, df = docx_to_csv(file)
   if status != "OK":
      st.error(status)
      st.stop()

   st.write(df)

   csv = convert_df(df)

   st.download_button(
      "Press to Download",
      csv,
      "file.csv",
      "text/csv",
      key='download-csv'
   )

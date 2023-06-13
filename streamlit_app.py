from collections import namedtuple
import altair as alt
import math
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

    #To convert to a string based IO:

    stringio = StringIO(file.getvalue().decode("utf-8"))

    #To read file as string:

    string_data = stringio.read()

    #Can be used wherever a "file-like" object is accepted:

    df= pd.read_csv(file)

    st.write(df)

    csv = convert_df(df)

    st.download_button(
    "Press to Download",
    csv,
    "file.csv",
    "text/csv",
    key='download-csv'
    )

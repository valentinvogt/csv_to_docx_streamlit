from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st

#importing required libraries

import streamlit as st

from io import StringIO 



#adding a file uploader

file = st.file_uploader("Please choose a file")

if file is not None:

    #To read file as bytes:

    bytes_data = file.getvalue()

    st.write(bytes_data)



    #To convert to a string based IO:

    stringio = StringIO(file.getvalue().decode("utf-8"))

    st.write(stringio)



    #To read file as string:

    string_data = stringio.read()

    st.write(string_data)



    #Can be used wherever a "file-like" object is accepted:

    df= pd.read_csv(file)

    st.write(df)

    st.download_button('Download CSV', df, 'text/csv')

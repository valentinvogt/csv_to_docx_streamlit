import streamlit as st
from src.parse_docx import parse_docx, adapt_data


@st.cache_data
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


st.title("Synchronbuch Converter")
file = st.file_uploader("Please choose a .docx file (not .doc)")

if file is not None:
    status, data = parse_docx(file)
    if status != "OK":
        st.error(status)
        st.stop()

    csv = convert_df(adapt_data(data))

    st.success("CSV file successfully created!")

    st.download_button(
        "Download",
        csv,
        f"{file.name.removesuffix('.docx')}.csv",
        "text/csv",
        key="download-csv",
    )

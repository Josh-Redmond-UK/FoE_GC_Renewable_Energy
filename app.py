import streamlit as st
import ee
st.set_page_config(page_title = "Homepage")

st.title("UK Renewable Energy Potential", anchor=None)

st.write(ee.Authenticate())
#### Page name w/ emoji for you to copy and paste
#### 🏡_Homepage.py



import streamlit as st
import ee
st.set_page_config(page_title = "Homepage")

title = "UK Renewable Energy Potential"
#title_md = f'<p font-size:12">{title}</p>'
#st.sidebar.markdown(title_md, unsafe_allow_html = True)

st.markdown("""
<style>
.big-font {
    font-size:35px !important;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<strong class='big-font'>Mapping the UK's Renewable Energy Potential</strong>", unsafe_allow_html=True)
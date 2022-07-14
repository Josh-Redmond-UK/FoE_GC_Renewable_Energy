import streamlit as st

with open('data.txt', 'r') as file:
    data = file.read()

st.markdown(data)

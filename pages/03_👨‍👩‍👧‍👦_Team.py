import streamlit as st

with open('~/website and profiles/data.txt', 'r') as file:
    data = file.read()

st.markdown(data)

# Dependencies
import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title = "UK Renewables Table")

# Page title
st.title("UK Renewables Table")

# Random numbers for data
data = pd.DataFrame(np.random.randint(7, 12000, size = (650)))

# Output
st.dataframe(data = data)

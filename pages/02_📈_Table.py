# Dependencies
import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title = "UK Renewables Table")

# Page title
st.title("UK Renewables Table")

# Read in county names
constituencies = pd.read_csv("constituencies_names.csv")
constituencies = constituencies.rename(columns = {"pcon19nm" : "Constituency"})

# Random numbers for data
data = pd.DataFrame(np.random.randint(7, 12000, size = (650, 5)), columns = ["Available area (sq.km)", "Expected output (MW)", "Other Output 1 (?)", "Other Output 2 (?)", "Other Output 3 (?)"])
data = data.set_index(constituencies["Constituency"])

# Output dataframe
st.dataframe(data = data.style.format({"Available area (sq.km)": "{:20,.0f}", 
                          "Expected output (MW)": "{:20,.0f}", 
                          "Other Output 1 (?)": "{:20,.0f}",
                          "Other Output 2 (?)":"{:20,.0f}",
                          "Other Output 3 (?)": "{:20,.0f}"}), height = 750)


# Calculate total potential
wind_output = data["Expected output (MW)"].sum()
#solar_output = data["Expected output (MW)"].sum()
st.markdown(f"The estimated total on-shore wind energy potential for the UK is: **{wind_output:,} MW**")
#st.write(f"The estimated total ground-mounted solar energy potential is: {solar_output}MW")



# Convert dataframe to csv, download button
@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')


csv = convert_df(data)

st.download_button(
   "Download .csv",
   csv,
   "EIGC22_tableoutput.csv",
   "text/csv",
   key='download-csv'
)
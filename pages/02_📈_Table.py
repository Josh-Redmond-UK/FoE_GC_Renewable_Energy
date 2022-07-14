# Dependencies
import streamlit as st
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(page_title = "UK Renewables Table")

# Page title
#st.title("UK Renewables Table")

# Read in county names
constituencies = pd.read_csv("constituencies_names.csv")
constituencies = constituencies.rename(columns = {"pcon19nm" : "Constituency"})

# Random numbers for data
data = pd.DataFrame(np.random.randint(7, 12000, size = (650, 4)), columns = ["Available wind area (sq.km)", "Expected wind output (MW)", "Available solar area (sq. km)", "Expected solar output (MW)"])

testframe = pd.read_csv("test_csv.csv")


testframe['Wind Energy Estimate (GW)'] = testframe['sum']/1000 * 19.8 / 1000
testframe['Solar Energy Estimate (GW)'] = testframe['sum']/1000 * 200 / 1000
testframe['Total Area Available for Devleopment (Km/2)'] = testframe['sum']/1000 

data = testframe[['Wind Energy Estimate (GW)', 'Solar Energy Estimate (GW)', 'Total Area Available for Devleopment (Km/2)', 'pcon19nm']]


#st.dataframe(testframe)


data = data.set_index(data["pcon19nm"])
data = data[['Wind Energy Estimate (GW)', 'Solar Energy Estimate (GW)', 'Total Area Available for Devleopment (Km/2)']]
data = data.rename_axis("Constituency")

# Put session state (exclusions) in sidebar
display_df = st.session_state['exclusion_buttons_side']
display_df = display_df.style.hide_columns()
st.sidebar.write(display_df.to_html(), unsafe_allow_html=True)

# Output dataframe
st.dataframe(data = data.style.format({"Available wind area (sq.km)": "{:20,.0f}", 
                          "Expected wind output (MW)": "{:20,.0f}", 
                          "Available solar area (sq. km)": "{:20,.0f}",
                          "Expected solar output (MW)":"{:20,.0f}"}), width = 1000, height = 750)


# Calculate total potential
potentials = pd.DataFrame()
potentials["Total wind energy potential (GW)"] = [data["Wind Energy Estimate (GW)"].sum()]
potentials["Total solar energy potential (GW)"] = [data["Solar Energy Estimate (GW)"].sum()]

# Output potentials dataframe
style = potentials.style.hide_index().format({"Total wind energy potential (GW)": "{:20,.0f}",
                                             "Total solar energy potential (GW)": "{:20,.0f}"})
st.write(style.to_html(), unsafe_allow_html=True)

# some whitespace to separate table from button
st.text("")

# Convert dataframe to csv, download button
@st.cache
def convert_df(df):
   return df.to_csv().encode('utf-8')

csv1 = convert_df(data)
csv2 = convert_df(potentials)

c1, c2 = st.columns(2)

with c1:
    st.download_button(
   "Download .csv",
   csv1,
   "EIGC22_tableoutput.csv",
   "text/csv",
   key='download-csv1'
)

# with c2:
#     st.download_button(
#    "Download potentials",
#    csv2,
#    "EIGC22_potentialsoutput.csv",
#    "text/csv",
#    key='download-csv2'
# )
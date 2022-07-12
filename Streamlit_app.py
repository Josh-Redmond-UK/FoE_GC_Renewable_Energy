from turtle import onclick
import streamlit as st
from streamlit_folium import folium_static
import ee
import geemap.eefolium as geemap
from utils import *
ee.Initialize()


wind_exclusions = ["Wind Speed",
"Transmission Lines",
"Aircraft Flightpath",
"Noise",
"Built Up Areas",
"Slope > 15"]

common_exclusions = ["Roads",
"Railway",
"Public Rights of Way",
"Heritage Sites",
"Existing Renewable Projects",
"Peatland",
"Protected Areas"]

solar_exclusions = ["Solar Insolation",
"Agricultural Land",
"Aspect",
"Slope > 10"]


st.title("UK Renewable Energy Potential Map", anchor=None)

m = geemap.Map(center=[55.3, 0], zoom=6)
uk_adm2 = ee.FeatureCollection("FAO/GAUL/2015/level2").filter("ADM0_CODE == 256")
m.addLayer(uk_adm2)
folium_static(m)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        mode = st.radio("Power Option", ["Solar", "Wind"])
    with col2:
        area = st.selectbox("Area", ["Cheshire", "Devonshire", "Cornwall"]) #on_change =area_change_callback, args={"Cheshire", uk_adm2, m})




with st.sidebar:
    with st.container():
        st.header("Toggle Exclusion Criteria")
        radio_button = st.radio("Scenarios", ["Preset 1", "Preset 2", "Custom"])
        if radio_button == "Custom":
            with st.expander("Options"):
                if mode == "Wind":
                    exclusion_options = common_exclusions+wind_exclusions
                else:
                    exclusion_options = common_exclusions+solar_exclusions

                for ex in exclusion_options:
                    st.checkbox(ex)
        st.download_button("Download Map", "null", f"{area}-{mode}.txt")
        #st.multiselect("Toggleable Criteria", wind_exclusions+common_exclusions)



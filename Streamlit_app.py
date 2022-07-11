import streamlit as st
from streamlit_folium import folium_static
import ee
import geemap.eefolium as geemap



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

m = geemap.Map()
folium_static(m)


mode = st.radio("Power Option", ["Solar", "Wind"])

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
        #st.multiselect("Toggleable Criteria", wind_exclusions+common_exclusions)



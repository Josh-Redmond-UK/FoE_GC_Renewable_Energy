from turtle import onclick
import streamlit as st
from streamlit_folium import folium_static
import ee



import geemap.eefolium as geemap
from utils import *

polys_list = load_csv_list("adm2_names.csv")[1:]


ee.Initialize()#st.secrets['EARTHENGINE_TOKEN'])



exclusions_dict = {"Wind Speed": ee.Image('projects/data-sunlight-311713/assets/wind_cutoff').lt(1),
"Slope": ee.Terrain.slope(ee.Image("USGS/SRTMGL1_003")).lt(15),
"Transmission Lines":ee.FeatureCollection('projects/data-sunlight-311713/assets/transmission').reduceToImage(properties= ['FEATCODE'], reducer= ee.Reducer.first()).unmask().lt(1)}

test_exclusions = list(exclusions_dict.keys())

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


with st.form("Parameters"):
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            mode = st.radio("Power Option", ["Solar", "Wind"])
        with col2:
            area = st.selectbox("Area", polys_list) #on_change =area_change_callback, args={"Cheshire", uk_adm2, m})
            go_button = st.form_submit_button("Draw Map")


    with st.sidebar:
        with st.container():
            st.header("Toggle Exclusion Criteria")
            radio_button = st.radio("Scenarios", ["Preset 1", "Preset 2", "Custom"])
            if radio_button == "Custom":
                with st.expander("Options"):
                    exclusion_buttons = {}
                    if mode == "Wind":
                        exclusion_options = test_exclusions
                    else:
                        exclusion_options = test_exclusions#common_exclusions+solar_exclusions

                    for ex in exclusion_options:
                        st.write(ex)
                        x = st.checkbox(ex)
                        exclusion_buttons[ex] = x
            if radio_button == "Preset 1":
                exclusion_buttons = {"Wind Speed":True, "Transmission Lines":True}
            if radio_button == "Preset 2":
                exclusion_buttons = {"Wind Speed":True, "Slope": True}
                    

            st.download_button("Download Map", "null", f"{area}-{mode}.txt")
            #st.multiselect("Toggleable Criteria", wind_exclusions+common_exclusions)


if go_button:
    m = geemap.Map(center=[55.3, 0], zoom=4)
    uk_adm2 = ee.FeatureCollection("FAO/GAUL/2015/level2").filter("ADM0_CODE == 256").filter(f"ADM2_NAME == '{area}'")
    m.addLayer(uk_adm2)
    m.centerObject(uk_adm2)
    image_exclusion = []
    for x in exclusion_buttons.keys():
        st.write(x)
        if exclusion_buttons[x]:
            image_exclusion.append(exclusions_dict[x])
            print(exclusions_dict[x])

    windpower_adj = compute_exclusions(image_exclusion, ee.Image('projects/data-sunlight-311713/assets/wind_power')).clip(uk_adm2)
    m.addLayer(windpower_adj)
    folium_static(m)



#Exclusion(label="test", exclusion = ee.Terrain.slope(ee.Image("CGIAR/SRTM90_V4")).gt(15))




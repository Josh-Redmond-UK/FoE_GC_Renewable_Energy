# Dependencies
import streamlit as st

# Set page config
st.set_page_config(page_title = "Map output", layout="wide")

from streamlit_folium import folium_static
import ee

import geemap.eefolium as geemap


from utils import *


# Load in datasets (that aren't in GEE)
polys_list = load_csv_list("constituencies_names.csv")[1:]


service_account = st.secrets['username']
credentials = ee.ServiceAccountCredentials(service_account, st.secrets['gcp_service_account'])
ee.Initialize(credentials)


# Intialize earth engine
#ee.Initialize()#st.secrets['EARTHENGINE_TOKEN'])

# Exclusion zones
exclusions_dict = {"Wind Speed": ee.Image('projects/data-sunlight-311713/assets/wind_cutoff').lt(1),
"Slope": ee.Terrain.slope(ee.Image("USGS/SRTMGL1_003")).lt(15),
"Transmission Lines":ee.FeatureCollection('projects/data-sunlight-311713/assets/transmission').reduceToImage(properties= ['FEATCODE'], reducer= ee.Reducer.first()).unmask().lt(1),
"Roads": ee.FeatureCollection('projects/data-sunlight-311713/assets/UK_Roads_Buffer_200m').reduceToImage(properties= ['FEATCODE'], reducer= ee.Reducer.first()).unmask().lt(1),
"Peatland": ee.FeatureCollection('projects/data-sunlight-311713/assets/merged_peatlands').reduceToImage(properties = ['Shape__Are'], reducer= ee.Reducer.first()).unmask().lt(1),
"Woodlands": ee.FeatureCollection('projects/data-sunlight-311713/assets/woodlands').reduceToImage(properties= ['FEATCODE'], reducer = ee.Reducer.first()).unmask().lt(1),
"Cycle Paths": ee.FeatureCollection('projects/data-sunlight-311713/assets/cyclenet').reduceToImage(properties= ['FID'], reducer= ee.Reducer.first()).unmask().lt(1),
"Railway": ee.FeatureCollection('projects/data-sunlight-311713/assets/traintracks').reduceToImage(properties = ['FEATCODE'], reducer = ee.Reducer.first()).unmask().lt(1)}

test_exclusions = list(exclusions_dict.keys())

wind_exclusions = ["Wind Speed",
"Transmission Lines",
"Aircraft Flightpath",
"Noise",
"Built Up Areas",
"Slope"]

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

# Streamlit formatting
st.title("UK Renewables Map", anchor=None)

with st.form("Parameters"):
    st.header("Map Options")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            mode = st.radio("Power Option", ["Solar", "Wind"])
        with col2:
            area = st.selectbox("Area", polys_list) #on_change =area_change_callback, args={"Cheshire", uk_adm2, m})
            go_button = st.form_submit_button("Draw Map")

        st.header("Toggle Exclusion Criteria")
        radio_button = st.radio("Scenarios", ["Maximum Exclusions", "Allow on Peatland", "Custom"])
        #   if radio_button == "Custom":
        with st.expander("Options"):
            exclusion_buttons = {}
            if mode == "Wind":
                exclusion_options = test_exclusions
            else:
                exclusion_options = test_exclusions#common_exclusions+solar_exclusions

            for ex in exclusion_options:
                #st.write(ex)
                x = st.checkbox(ex)
                exclusion_buttons[ex] = x
        if radio_button == "Maximum Exclusions":
            exclusion_buttons = {"Wind Speed":True, "Transmission Lines":True, "Roads":True, "Slope": True, "Peatland": True, "Woodlands":True, "Cycle Paths": True, "Railway": True}
        if radio_button == "Allow on Peatland":
            exclusion_buttons = {"Wind Speed":True, "Transmission Lines":True, "Roads":True, "Slope": True, "Peatland": False, "Woodlands":True, "Cycle Paths": True, "Railway": True}
                

        #st.multiselect("Toggleable Criteria", wind_exclusions+common_exclusions)





if go_button:
    m = geemap.Map(center=[55.3, 0], zoom=6)
    uk_adm2 = ee.FeatureCollection("projects/data-sunlight-311713/assets/Westminster_Parliamentary_Constituencies_December_2019_Boundaries_UK_BUC").filter(f"pcon19nm == '{area}'")
    m.addLayer(uk_adm2, {}, f"{area}", True, 0.5)
    m.centerObject(uk_adm2)
    image_exclusion = []
    for x in exclusion_buttons.keys():
        if exclusion_buttons[x]:
            image_exclusion.append(exclusions_dict[x])
            #st.write(exclusions_dict[x])

    windpower_adj = compute_exclusions(image_exclusion, ee.Image('projects/data-sunlight-311713/assets/wind_power')).clip(uk_adm2)
    windpower_adj = windpower_adj.updateMask(windpower_adj.gt(0))
    
    pix_area = windpower_adj.pixelArea().reduceRegion(
  reducer= ee.Reducer.sum(),
  geometry= uk_adm2,
  scale= 10).get('area').getInfo()

    st.write("total output", pix_area/1000*19, "MW")


    windpower_cand_zones = windpower_adj.gt(0).pixelArea()
    m.addLayer(windpower_adj, {"min":1, "max":1000})

    folium_static(m, width=1400, height=700)
    st.download_button("Download Map", "null", f"{area}-{mode}.txt")




#Exclusion(label="test", exclusion = ee.Terrain.slope(ee.Image("CGIAR/SRTM90_V4")).gt(15))
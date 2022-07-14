# Dependencies
import streamlit as st
from google.oauth2 import service_account
import json, tempfile
# Set page config
st.set_page_config(page_title = "Map output", layout="wide")

from streamlit_folium import folium_static, st_folium
import ee

import geemap as geemap


from utils import *


# Load in datasets (that aren't in GEE)
polys_list = load_csv_list("constituencies_names.csv")[1:]




service_account = st.secrets['service_account']

data = {}
data['type'] = st.secrets['other_keys']['type']
data['project_id'] = st.secrets['other_keys']['project_id']
data['private_key_id'] = st.secrets['other_keys']['private_key_id']
data['private_key'] = st.secrets['other_keys']['private_key']
data['client_email'] = st.secrets['other_keys']['client_email']
data['client_id'] = st.secrets['other_keys']['client_id']
data['auth_uri'] = st.secrets['other_keys']['auth_uri']
data['token_uri'] = st.secrets['other_keys']['token_uri']
data['auth_provider_x509_cert_url'] = st.secrets['other_keys']['auth_provider_x509_cert_url']
data['client_x509_cert_url'] = st.secrets['other_keys']['client_x509_cert_url']


tfile = tempfile.NamedTemporaryFile(mode="w+")
json.dump(data, tfile)
tfile.flush()
credentials = ee.ServiceAccountCredentials(service_account, tfile.name)
ee.Initialize(credentials)


#credentials = service_account.Credentials.from_service_account_info(st.secrets['username'], st.secrets["gcp_service_account"])
#ee.Initialize()

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
"Railway": ee.FeatureCollection('projects/data-sunlight-311713/assets/traintracks').reduceToImage(properties = ['FEATCODE'], reducer = ee.Reducer.first()).unmask().lt(1),
"Areas of Natural Beauty": ee.FeatureCollection("projects/data-sunlight-311713/assets/Areas_of_Outstanding_Natural_Beauty_England").reduceToImage(properties= ['stat_area'], reducer= ee.Reducer.first()).unmask().lt(1),
"Protected Areas": ee.FeatureCollection("projects/data-sunlight-311713/assets/gb_protected_areas_nobuffer").reduceToImage(properties= ['Shape_Area'], reducer= ee.Reducer.first()).unmask().gt(0).eq(0),
"Surface Water":ee.FeatureCollection('projects/data-sunlight-311713/assets/UK_SurfaceWater_Area_Buffer_50m').reduceToImage(properties= ['FEATCODE'], reducer= ee.Reducer.first()).unmask().lt(1),
"Cultural Sites": ee.FeatureCollection('projects/data-sunlight-311713/assets/england_culturalsites').reduceToImage(properties = ['ListEntry'], reducer = ee.Reducer.first()).unmask().lt(1),
"Parks and Green Space": ee.FeatureCollection("projects/data-sunlight-311713/assets/GreenspaceEngArea").reduceToImage(properties= ['areaHa'], reducer= ee.Reducer.first()).unmask().lt(1)}

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
"Protected Areas",
"Areas of Natural Beauty"]

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
            exclusion_buttons = {"Wind Speed":True, "Transmission Lines":True, "Roads":True, "Slope": True, "Peatland": True, "Woodlands":True, "Cycle Paths": True, "Railway": True, "Protected Areas":True, 'Areas of Natural Beauty':True, "Surface Water": True, "Cultural Sites": True, "Parks and Green Space":True}
        if radio_button == "Allow on Peatland":
            exclusion_buttons = {"Wind Speed":True, "Transmission Lines":True, "Roads":True, "Slope": True, "Peatland": False, "Woodlands":True, "Cycle Paths": True, "Railway": True, "Protected Areas":True, 'Areas of Natural Beauty':True, "Surface Water": True}
                

        #st.multiselect("Toggleable Criteria", wind_exclusions+common_exclusions)
        go_button = st.form_submit_button("Draw Map")






if go_button:

    m = geemap.Map(center=[55.3, 0], zoom=6)
    uk_adm2 = ee.FeatureCollection("projects/data-sunlight-311713/assets/Westminster_Parliamentary_Constituencies_December_2019_Boundaries_UK_BUC").filter(f"pcon19nm == '{area}'")
    m.centerObject(uk_adm2)
    image_exclusion = []

    for x in exclusion_buttons.keys():
    # st.write(x)
    # st.write(exclusion_buttons[x])
        if exclusion_buttons[x]:
            image_exclusion.append(exclusions_dict[x])
    #     st.write(exclusions_dict[x])

    if mode == "Solar":
        power = ee.Image('projects/data-sunlight-311713/assets/PV_Average')
        minvis = 500
        maxvis = 1000
    else:
        power = ee.Image('projects/data-sunlight-311713/assets/wind_power')
        minvis = 1
        maxvis = 1000

    windpower_adj = compute_exclusions(image_exclusion, power).clip(uk_adm2)
    windpower_adj = windpower_adj.updateMask(windpower_adj.gt(0))
    
    pix_area = windpower_adj.pixelArea().reduceRegion(
    reducer= ee.Reducer.sum(),
    geometry= uk_adm2,
    scale= 50, maxPixels=99999999999999999, bestEffort=True).get('area').getInfo()

# st.write("total output", pix_area/1000*19, "MW")

    empty = ee.Image().byte()

    outline = empty.paint(
    featureCollection= uk_adm2,
    color= 1,
    width= 3
    )
    m.addLayer(outline, {}, f"{area}", True, 0.5)




    windpower_cand_zones = windpower_adj.gt(0).pixelArea()


    m.addLayer(windpower_adj, {"min":minvis, "max":maxvis, "palette":['#140b34', '#84206b', '#e55c30', '#f6d746']})
    m.add_colorbar_branca(colors=['#140b34', '#84206b', '#e55c30', '#f6d746'], vmin=minvis, vmax=maxvis, layer_name="Potential Power")
    m.to_streamlit()
    #folium_static(m, height=700)
    st.download_button("Download Map", "null", f"{area}-{mode}.txt")




#Exclusion(label="test", exclusion = ee.Terrain.slope(ee.Image("CGIAR/SRTM90_V4")).gt(15))
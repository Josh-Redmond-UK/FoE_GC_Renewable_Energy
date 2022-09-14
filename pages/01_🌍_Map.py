# Dependencies
import streamlit as st
from google.oauth2 import service_account
import json, tempfile
import pandas as pd
import os
# Set page config
st.set_page_config(page_title = "Map output", layout="wide")

from streamlit_folium import folium_static, st_folium
import ee

import geemap.eefolium as geemap


from utils import *


# Load in datasets (that aren't in GEE)
polys_list = load_csv_list("constituencies_names.csv")[1:]
lad_list = load_csv_list("local_authorities_name.csv")[1:]



# service_account = st.secrets['service_account']
junkstring = '''
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

tfile = tempfile.NamedTemporaryFile(mode="w+")
json.dump(data, tfile)
tfile.flush()
credentials = ee.ServiceAccountCredentials(service_account, tfile.name)
ee.Initialize(credentials)'''


#credentials = service_account.Credentials.from_service_account_info(st.secrets['username'], st.secrets["gcp_service_account"])
ee.Initialize()

# Intialize earth engine
#ee.Initialize()#st.secrets['EARTHENGINE_TOKEN'])

# Exclusion zones
exclusions_dict = {"Wind Speed": ee.Image('projects/data-sunlight-311713/assets/wind_cutoff').lt(1),
"Slope": ee.Terrain.slope(ee.Image("USGS/SRTMGL1_003")).lt(15),
"Slope > 10": ee.Terrain.slope(ee.Image("USGS/SRTMGL1_003")).lt(10),
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
"Parks and Green Space": ee.FeatureCollection("projects/data-sunlight-311713/assets/GreenspaceEngArea").reduceToImage(properties= ['areaHa'], reducer= ee.Reducer.first()).unmask().lt(1),
"Functional Sites": ee.FeatureCollection('projects/data-sunlight-311713/assets/Functional_sites').reduceToImage(properties= ['FEATCODE'], reducer= ee.Reducer.first()).unmask().lt(1),
"Built Up Areas": get_build_up_area_buffer(100).unmask().lt(1),
"Existing Solar PV": ee.FeatureCollection('projects/data-sunlight-311713/assets/solar_pv').reduceToImage(properties= ['FID'], reducer = ee.Reducer.first()).unmask().lt(1),
"Existing Other Renewable":ee.FeatureCollection('projects/data-sunlight-311713/assets/other_renewables').reduceToImage(properties= ['FID'], reducer= ee.Reducer.first()).unmask().lt(1),
"Existing Onshore Wind": ee.FeatureCollection('projects/data-sunlight-311713/assets/onshore_wind').reduceToImage(properties= ['FID'], reducer= ee.Reducer.first()).unmask().lt(1),
"Flood Risk Zone 2": ee.FeatureCollection('users/Josh_Redmond/EA_FloodMapForPlanningRiversAndSeaFloodZone2_SHP_Full').reduceToImage(properties= ['st_area_sh'], reducer= ee.Reducer.first()).unmask().lt(1),
"Flood Risk Zone 3": ee.FeatureCollection('users/Josh_Redmond/EA_FloodMapForPlanningRiversAndSeaFloodZone3_SHP_Full').reduceToImage(properties= ['st_area_sh'], reducer= ee.Reducer.first()).unmask().lt(1)
}

test_exclusions = list(exclusions_dict.keys())

wind_exclusions = ["Wind Speed",
"Transmission Lines",
"Aircraft Flightpath",
"Noise",
"Built Up Areas",
"Slope",
"Existing Onshore Wind",
"Existing Other Renewable"]

common_exclusions = ["Roads",
"Railway",
#"Public Rights of Way",
#"Heritage Sites",
"Peatland",
"Protected Areas",
"Areas of Natural Beauty",
"Woodlands",
"Cycle Paths",
"Surface Water",
"Cultural Sites",
"Parks and Green Space",
"Functional Sites",
]

solar_exclusions = ["Slope > 10",
"Existing Solar PV"]

# Streamlit formatting
#st.title("UK Renewables Map", anchor=None)

geometry_mode = st.selectbox("Local Area Type", ['Constituencies', 'Local Authorities'])

mode = st.radio("Power Option", ["🌞 Solar", "💨 Wind"])

with st.form("Parameters"):
    st.header("Map Options")
    with st.container():
       # col1, col2 = st.columns(2)
        #with col1:
       # with col2:
        if geometry_mode == "Constituencies":
  
            area = st.selectbox("Area", polys_list) #on_change =area_change_callback, args={"Cheshire", uk_adm2, m})
            
        else:
            area =st.selectbox("Area", lad_list)
        st.session_state['geometry'] = area

        st.header("Toggle Exclusion Criteria")
        radio_button = st.radio("Scenarios", ["Maximum Exclusions", "Allow on Peatland", "Custom"])
        #   if radio_button == "Custom":
        with st.expander("Options"):
            exclusion_buttons = {}
            if mode == "💨 Wind":
                key_list = common_exclusions+wind_exclusions
                #test_exclusions = list({exclusions_dict[k] for k in key_list}.keys())
                test_exclusions = key_list
                exclusion_options = test_exclusions
            else:
                key_list = common_exclusions+solar_exclusions
                test_exclusions = key_list

             #   test_exclusions = list({exclusions_dict[k] for k in key_list}.keys())
                exclusion_options = test_exclusions

            for ex in exclusion_options:
                #st.write(ex)
                x = st.checkbox(ex)
                exclusion_buttons[ex] = x
                
        if radio_button == "Maximum Exclusions":
            exclusion_buttons = {key:True for key in list(exclusions_dict.keys())}
        if radio_button == "Allow on Peatland":
            exclusion_buttons = {key:True for key in list(exclusions_dict.keys())}
            exclusion_buttons['Peatland'] = False
                

        #st.multiselect("Toggleable Criteria", wind_exclusions+common_exclusions)
        go_button = st.form_submit_button("Draw Map")

# Save exclusions buttons output in session state to display between pages
#exclusion_buttons_side = pd.DataFrame.from_dict(exclusion_buttons, orient = "index")

#if 'exclusion_buttons_side' not in st.session_state:
#    st.session_state['exclusion_buttons_side'] = exclusion_buttons_side
#if go_button:
#    st.session_state['exclusion_buttons_side'] = exclusion_buttons_side

# Make the true/false dict emojis
#torf = {True : "❌", False : "✅"}

#display_df = st.session_state['exclusion_buttons_side']
#display_df[0] = display_df[0].map(torf)
#display_df = display_df.style.hide_columns()

#st.sidebar.write(display_df.to_html(), unsafe_allow_html=True)



#st.sidebar.dataframe(display_df)




if go_button:

    m = geemap.Map(center=[55.3, 0], zoom=6)
    if geometry_mode == "Constituencies":
        uk_adm2_all = ee.FeatureCollection("projects/data-sunlight-311713/assets/Westminster_Parliamentary_Constituencies_December_2019_Boundaries_UK_BUC")#.filter(f"pcon19nm == '{area}'")
        uk_adm2 = uk_adm2_all.filter(f"pcon19nm == '{area}'")
    else:
        uk_adm2_all = ee.FeatureCollection("projects/data-sunlight-311713/assets/local_authorities_UK")#.filter(f"pcon19nm == '{area}'")
        uk_adm2 = uk_adm2_all.filter(f"LAD21NM == '{area}'")

    m.centerObject(uk_adm2)
    image_exclusion = []

    for x in exclusion_buttons.keys():
    # st.write(x)
    # st.write(exclusion_buttons[x])
        if exclusion_buttons[x]:
            image_exclusion.append(exclusions_dict[x])
    #     st.write(exclusions_dict[x])

    if mode == "🌞 Solar":
        power = ee.Image('projects/data-sunlight-311713/assets/PV_Average')
        minvis = 500
        maxvis = 1500
    else:
        power = ee.Image('projects/data-sunlight-311713/assets/wind_power')
        minvis = 1
        maxvis = 1000

    power = compute_exclusions(image_exclusion, power)
    power = power.updateMask(power.gt(0))

    st.session_state['power'] = power
    power = power.clip(uk_adm2)
    st.session_state['bounds'] = uk_adm2#_all

    empty = ee.Image().byte()

    outline = empty.paint(
    featureCollection= uk_adm2,
    color= 1,
    width= 3
    )
    m.addLayer(outline, {}, f"{area}", True, 0.5)




    m.addLayer(power, {"min":minvis, "max":maxvis, "palette":['#140b34', '#84206b', '#e55c30', '#f6d746']})
    m.add_colorbar(colors=['#140b34', '#84206b', '#e55c30', '#f6d746'], vmin=minvis, vmax=maxvis, layer_name="Potential Power")

    m.addLayerControl() 
    if mode == '🌞 Solar':
        st.write("Map Power Units in kWh/kWp")
    else:
        st.write("Map Power Units in W/M2")
    folium_static(m, width=800, height=700)



    try:
        os.remove("test_csv.csv")
    except:
        pass


    #power = st.session_state['power']
    geom_mode = st.session_state['geometry']

    geemap.zonal_statistics(power.gt(0).multiply(ee.Image.constant(30)), st.session_state['bounds'] , "test_csv.csv", statistics_type='SUM', scale=30)




    # try:
    # Page title
    #st.title("UK Renewables Table")

    # Read in county names
    constituencies = pd.read_csv("test_csv.csv")
    #st.write(print(constituencies))
    constituencies['Wind Energy Estimate (GW)'] = constituencies['sum']/1000 * 19.8 / 1000
    constituencies['Solar Energy Estimate (GW)'] = constituencies['sum']/1000 * 200 / 1000
    constituencies['Total Area Available for Devleopment (Km/2)'] = constituencies['sum']/1000 

    try:
        constituencies = constituencies.rename(columns = {"pcon19nm" : "Constituency"})
        #constituencies.set_index(constituencies['Constituency'])
        constituencies = constituencies[['Constituency', 'Wind Energy Estimate (GW)', 'Solar Energy Estimate (GW)', 'Total Area Available for Devleopment (Km/2)']]

    except:
        constituencies = constituencies.rename(columns = {"LAD21NM" : "Local Authority"})
        #constituencies.set_index(constituencies['Local Authority'])
        constituencies = constituencies[['Local Authority', 'Wind Energy Estimate (GW)', 'Solar Energy Estimate (GW)', 'Total Area Available for Devleopment (Km/2)']]



    # constituencies = constituencies["sum"]
    st.dataframe(constituencies)
    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csvDownload = convert_df(constituencies)
    st.download_button(
    "Download .csv",
    csvDownload,
    "Renewable Energy Potential.csv",
    "text/csv",
    key='download-csv1'   )


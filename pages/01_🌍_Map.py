# Dependencies
import streamlit as st
from google.oauth2 import service_account
import json, tempfile
import pandas as pd
import os
import multiprocessing
# Set page config
st.set_page_config(page_title = "Map output", layout="wide")

from streamlit_folium import folium_static, st_folium
import ee

import geemap.eefolium as geemap


from utils import *

#Get rasters for the renewable power potentials
pvPotential = solarPowerRaster()
turbinePotential = windPowerRaster()

# Load in datasets (that aren't in GEE) containing constituency/LAD names
polys_list = load_csv_list("constituencies_names.csv")[1:]
lad_list = load_csv_list("local_authorities_name.csv")[1:]


### This is used for authenticating when the app is deployed, we dont need it right now 
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

# Initialise with the high volume API for faster queries
#credentials = service_account.Credentials.from_service_account_info(st.secrets['username'], st.secrets["gcp_service_account"])
ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')


# Intialize earth engine
#ee.Initialize()#st.secrets['EARTHENGINE_TOKEN'])

# Exclusion zones
# Each entry is a string describing the exclusion as the key, and a google earth engine integer image with values 0 and 1 where 1 is "can build" and 0 is "cant build"
# We multiply the list of all active exclusions together to get an area where none of them are active (i.e. where it is ok to build)
exclusions_dict = getExclusionsDict()
test_exclusions = list(exclusions_dict.keys())

# Some exclusions are only valid for certain power types, so they are split into different lists here
# When the user selects wind or solar, the common and the relevant specific lists are concatenated 
# to produce a list of the correct set of exclusion criteria which can be individually toggled


## Create the basic UI here - allow users to select between different geometry and power types
geometry_mode = st.selectbox("Local Area Type", ['Constituencies', 'Local Authorities'])

mode = st.radio("Power Option", ["🌞 Solar", "💨 Wind"])

with st.form("Parameters"):
    st.header("Map Options")
    with st.container():
       # col1, col2 = st.columns(2)
        #with col1:
       # with col2:
        if geometry_mode == "Constituencies":
  
            area = st.selectbox("Area", load_csv_list("constituencies_names.csv")[1:]) 
            
        else:
            area =st.selectbox("Area", load_csv_list("local_authorities_name.csv")[1:])
        st.session_state['geometry'] = area

        st.header("Toggle Exclusion Criteria")
        radio_button = st.radio("Scenarios", ["Maximum Exclusions", "Allow on Peatland", "Custom"])
        #   if radio_button == "Custom":
        with st.expander("Options"):
            exclusion_buttons = {}
            if mode == "💨 Wind":
                key_list = getExclusions("common")+getExclusions("wind") #common_exclusions+wind_exclusions
                test_exclusions = key_list
                exclusion_options = test_exclusions
            else:
                key_list = getExclusions("common") + getExclusions("solar") #common_exclusions+solar_exclusions
                test_exclusions = key_list
                exclusion_options = test_exclusions

            for ex in exclusion_options:
                x = st.checkbox(ex)
                exclusion_buttons[ex] = x
                
        if radio_button == "Maximum Exclusions":
            exclusion_buttons = {key:True for key in list(exclusions_dict.keys())}
        if radio_button == "Allow on Peatland":
            exclusion_buttons = {key:True for key in list(exclusions_dict.keys())}
            exclusion_buttons['Peatland'] = False
                

        go_button = st.form_submit_button("Draw Map")



if go_button:
    with st.spinner("Generating Renewable Potential Map"):
        # Select the correct geometry type and the specific geometry within that set according to user input
        if geometry_mode == "Constituencies":
            uk_adm2_all = constituenciesVector()
            activeGeom = uk_adm2_all.filter(f"pcon19nm == '{area}'")
        else:
            uk_adm2_all = ladsVector()
            activeGeom = uk_adm2_all.filter(f"LAD21NM == '{area}'")

        st.session_state['NationalGeometries'] = uk_adm2_all
        image_exclusion = []

        for x in exclusion_buttons.keys():
            if exclusion_buttons[x]:
                # Create a list of the active exclusions to multiply together 
                image_exclusion.append(exclusions_dict[x])
        if mode == "🌞 Solar":
            power = pvPotential
            minvis = 500
            maxvis = 1500
        else:
            power = turbinePotential
            minvis = 1
            maxvis = 1000

        exclusions = compute_exclusions(image_exclusion)
        localPower = minimumMappingUnit(getPowerLocal(activeGeom, exclusions, power))
        
        st.session_state['exclusions'] = exclusions
        st.session_state['geometryMode'] = geometry_mode
        st.session_state['power'] = localPower   
        st.session_state['bounds'] = activeGeom#_all
        m = getMap(localPower, activeGeom, area, minvis, maxvis)
        
        # 
        developmentArea = usableAreaPerGeom(activeGeom, localPower)

    if mode == '🌞 Solar':
        st.write("Map Power Units in kWh/kWp")
    else:
        st.write("Map Power Units in W/M2")

    # Generate the map and display with the active geometry and power raster
    folium_static(m, width=800, height=700)

    # Now get the usable area and power projections
    displayPowerOverview(activeGeom, exclusions, area)

import streamlit as st
from google.oauth2 import service_account
import json, tempfile
import pandas as pd
import os
import multiprocessing
# Set page config
st.set_page_config(page_title = "Map output", layout="wide")

import ee

from utils import *

st.title("Table View")

if "exclusions" not in st.session_state:
    st.write("Please use the map view to generate a set of exclusion criteria before using the table view")
else:
    with st.spinner("Generating Table, this might take a while..."):
        
        #Get rasters for the renewable power potentials
        pvPotential = solarPowerRaster()
        turbinePotential = windPowerRaster()

        # Load in datasets (that aren't in GEE) containing constituency/LAD names
        polys_list = load_csv_list("constituencies_names.csv")[1:]
        lad_list = load_csv_list("local_authorities_name.csv")[1:]

        ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')


        exclusions = st.session_state['exclusions']
        geometry_mode = st.session_state['geometryMode']


        solarPower = solarPowerRaster()
        windPower = windPowerRaster()

        if geometry_mode == "Constituencies":
            nameIndex = 'pcon19nm'
        else:
            nameIndex = 'LAD21NM'

        geometries = st.session_state['NationalGeometries']
        geomNames = geometries.aggregate_array(nameIndex).getInfo()

        #progressTooltip = st.write("Progress...")
        numGeoms = len(geomNames)


        progress = 0.0
        progressBar = st.progress(progress)

        names = []
        solarPotentials = []
        windPotentials = []
        developmentAreas = []

        for idx, n in enumerate(geomNames):
            geomUpdate = st.text(f"Geometry {idx+1} of {numGeoms}")
            activeGeom = geometries.filter(f"{nameIndex} == '{n}'")
            try:
                solarPotential = getGeomPotential(activeGeom, exclusions, pvPotential)
                windPotential = getGeomPotential(activeGeom, exclusions, turbinePotential)
            except:
                solarPotential = 0
                windPotential = 0
            solarPotentials.append(solarPotential)
            windPotentials.append(windPotential)
            progress += 1/numGeoms
            progressBar.progress(progress)
            #del(geomUpdate)

        resultsFrame = pd.dataFrame([names, solarPotentials, windPotentials], index=["Name", "Solar Power Potential", "Wind Power Potential"])
    #del(progressTooltip)
    del(progressBar)
    st.dataframe(resultsFrame)

    @st.cache
    def convert_df(df):
        return df.to_csv().encode('utf-8')

    csvDownload = convert_df(resultsFrame)
    st.download_button(
    "Download .csv",
    csvDownload,
    "Renewable Energy Potential.csv",
    "text/csv",
    key='download-csv1'   )

import streamlit as st
from streamlit_folium import folium_static
import ee
import geemap.eefolium as geemap



def area_change_callback(name, features, map):
    current_geom = features.filter(f"ADM2_NAME == '{name}'")
    map.center = current_geom.centroid(20).getinfo()
    

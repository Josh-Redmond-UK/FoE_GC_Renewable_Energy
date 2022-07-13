import streamlit as st
from streamlit_folium import folium_static
import ee
import geemap.eefolium as geemap
import csv
import pandas as pd



def give_adm2_list():
    []


def area_change_callback(name, features, map):
    current_geom = features.filter(f"ADM2_NAME == '{name}'")
    x, y = current_geom.centroid(20).getinfo()
    map.setCenter = [x,y,6]
    

def load_csv_list(path):
    return  list(pd.read_csv(path)['ADM2_NAME'])



class Exclusion():
    def __init__(self, exclusion, label):
        self.button = st.checkbox(label)
        self.ctieria = exclusion


        #self.criteria = criteria


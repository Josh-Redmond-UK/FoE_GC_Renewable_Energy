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
    try:
        return  list(pd.read_csv(path)['pcon19nm'])
    except:
        return  list(pd.read_csv(path)['LAD21NM'])


def get_build_up_area_buffer(distance=200):
    landcover = ee.ImageCollection("ESA/WorldCover/v100").first()

    urban_land = landcover.eq(50)
    cost_surface = ee.Image.constant(1)
    proj = ee.Projection(landcover.projection())

    build_dist = cost_surface.reproject(proj).cumulativeCost(urban_land, distance)
    buffer = build_dist.add(1).gt(0)
    return buffer

class Exclusion():
    def __init__(self, exclusion, label):
        self.button = st.checkbox(label)
        self.ctieria = exclusion


        #self.criteria = criteria

def compute_exclusions(exclusions, base):
    for e in exclusions:
        base = base.multiply(e)

    return base

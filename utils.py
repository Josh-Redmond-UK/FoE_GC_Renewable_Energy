
import streamlit as st
from streamlit_folium import folium_static
import ee
import geemap.eefolium as geemap
import csv
import pandas as pd
import logging
from retry import retry
import geopy



def solarPowerRaster():
    return ee.Image('projects/data-sunlight-311713/assets/PV_Average')

def windPowerRaster():
    return ee.Image('projects/data-sunlight-311713/assets/wind_power')

def constituenciesVector():
    return ee.FeatureCollection("projects/data-sunlight-311713/assets/Westminster_Parliamentary_Constituencies_December_2019_Boundaries_UK_BUC")

def ladsVector():
    return ee.FeatureCollection("projects/data-sunlight-311713/assets/local_authorities_UK")#.filter(f"pcon19nm == '{area}'")


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



def postcodeToGeom(postcode, geometries):
    geocoder = geopy.geocoders.Nominatim(user_agent="jr725@exeter.ac.uk")
    latlon = geocoder.geocode({"postalcode":postcode})[-1]
    activePoint = ee.Geometry.Point(latlon[1], latlon[0])
    activeGeom = ee.Feature(geometries.filterBounds(activePoint).first())
    return activeGeom



def getExclusionsDict():
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
    #"Existing Other Renewable":ee.FeatureCollection('projects/data-sunlight-311713/assets/other_renewables').reduceToImage(properties= ['FID'], reducer= ee.Reducer.first()).unmask().lt(1),
    "Existing Onshore Wind": ee.FeatureCollection('projects/data-sunlight-311713/assets/onshore_wind').reduceToImage(properties= ['FID'], reducer= ee.Reducer.first()).unmask().lt(1),
    "Flood Risk Zone 2": ee.FeatureCollection('users/Josh_Redmond/EA_FloodMapForPlanningRiversAndSeaFloodZone2_SHP_Full').reduceToImage(properties= ['st_area_sh'], reducer= ee.Reducer.first()).unmask().lt(1),
    "Flood Risk Zone 3": ee.FeatureCollection('users/Josh_Redmond/EA_FloodMapForPlanningRiversAndSeaFloodZone3_SHP_Full').reduceToImage(properties= ['st_area_sh'], reducer= ee.Reducer.first()).unmask().lt(1),
    #"High Grade Agricultural":
    "England National Parks": ee.FeatureCollection('projects/data-sunlight-311713/assets/EnglandNationalParks').reduceToImage(properties= ['code'], reducer= ee.Reducer.first()).unmask().lt(1)
    }

    return exclusions_dict

def getExclusions(type="common"):
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
    "England National Parks"
    ]

    solar_exclusions = ["Slope > 10",
    "Existing Solar PV"]

    listDict = {"solar":solar_exclusions, "common":common_exclusions, "wind":wind_exclusions}

    return listDict[type]




def compute_exclusions(exclusions):
    base = ee.Image.constant(1)
    for e in exclusions:
        base = base.multiply(e)

    return base

def computePowerAreaRequests(FeatureCollection, exclusions, power):

    areas = FeatureCollection.aggregate_array('.geo').getInfo()
    try:
        names = FeatureCollection.aggregate_array('pcon19nm').getInfo()
    except:
        names = FeatureCollection.aggregate_array('LAD21NM').getInfo()


    rasters = [raster for r in range(len(areas))]
    print(names, "done")
    requests =  [areas, names, rasters]
    return pd.DataFrame(requests).T

def renewablePotential(activeGeom, exclusions):  
    #solarExclusions = [exclusionsDict[x] for x in solarExclusions]

    windPotential = windPowerRaster()
    solarPotential = solarPowerRaster()
    localWind = windPotential.multiply(exclusions).reduceRegion(ee.Reducer.sum(), activeGeom).getInfo()['b1']
    localSolar = solarPotential.multiply(exclusions).reduceRegion(ee.Reducer.sum(), activeGeom).getInfo()['b1']

    totalArea = usableAreaPerGeom(activeGeom, windPotential.gt(0).Or(solarPotential.gt(0)))

    testdict =  {"Development Area": totalArea, "Solar Potential": localSolar, "Wind Potential": localWind}#jsonify(DevelopmentArea = totalArea, SolarPotential = localSolar, windPotential = localWind)
    return testdict




def displayPowerOverview(activeGeom, exclusions, area):
    with st.spinner("Generating Area Statistics"):

        summary = renewablePotential(activeGeom, exclusions)
        
        powerSummary = st.container()
        powerSummary.header(f"Summary of Renewable Potential in {area}")
        col1, col2, col3 = st.columns(3)

        with col1:
            totalArea = st.container()
            totalArea.subheader("Total Area Available for Development")
            totalArea.text(f"{summary['Development Area']/1000} KM2")

        with col2:
            solarPotential = st.container()
            solarPotential.subheader("Solar Power Potential with Current Exclusions")
            solarPotential.text(f"{summary['Solar Potential']} GW")
        
        with col3:
            windPotential = st.container()
            windPotential.subheader("Wind Power Potential with Current Exclusions")
            windPotential.text(f"{summary['Wind Potential']} GW")

def getGeomPotential(geometry, exclusions, raster):

    return minimumMappingUnit(raster.multiply(exclusions)).reduceRegion(ee.Reducer.sum(), geometry).getInfo()


def minimumMappingUnit(raster, size=10):
    mmuMask = raster.gt(0).connectedPixelCount().gte(size)
    return raster.updateMask(mmuMask)

#@retry(tries=10, delay=1, backoff=2)
def usableAreaPerGeom(geom, raster):
    #raster = args[2]
    #geom = args[0]
    try: 
        return minimumMappingUnit(raster).pixelArea().clip(geom).reproject(raster.projection()).reduceRegion(ee.Reducer.sum(), geom).getInfo()['area']
    except:
        return 0

def totalPowerPerGeom(geom, raster):
    try: 
        return minimumMappingUnit(raster).clip(geom).reproject(raster.projection()).reduceRegion(ee.Reducer.sum(), geom).getInfo()['b1']
    except:
        return 0


def getPowerLocal(geometry, exclusions, power):
    localPower = minimumMappingUnit(power.multiply(exclusions)).clip(geometry)
    return localPower.updateMask(localPower.gt(0))

def getMap(localPower, activeGeometry, areaName, minVis, maxVis):
    
    m = geemap.Map(center=[55.3, 0], zoom=6)
    m.centerObject(activeGeometry)
    empty = ee.Image().byte()

    outline = empty.paint(
    featureCollection= activeGeometry,
    color= 1,
    width= 3
    )
    m.addLayer(outline, {}, f"{areaName}", True, 0.5)
    m.addLayer(localPower, {"min":minVis, "max":maxVis, "palette":['#140b34', '#84206b', '#e55c30', '#f6d746']})
    m.add_colorbar(colors=['#140b34', '#84206b', '#e55c30', '#f6d746'], vmin=minVis, vmax=maxVis, layer_name="Potential Power")
    m.addLayerControl() 
    return m

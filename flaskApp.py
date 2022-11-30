from utils import *
from flask import Flask
from flask import jsonify
app = Flask(__name__)
ee.Initialize(opt_url='https://earthengine-highvolume.googleapis.com')
@app.route('/<postcode>')
def renewablePotential(postcode):  
    ladGeometries = ladsVector()
        #LADs = 
    activeGeom = ee.Feature(postcodeToGeom(postcode, ladGeometries)).geometry() ## Works with LAD only for near you page

    # Write utils default exclusions
    exclusionsDict = getExclusionsDict()
    windExclusions = getExclusions("wind") +  getExclusions("common")
    solarExclusions = getExclusions("solar")+ getExclusions("common")

    windExclusionImages = []
    solarExclusionImages = []
    for x in windExclusions:
        try:
            windExclusionImages.append(exclusionsDict[x])
        except:
            pass
    for x in solarExclusions:
        try:
            solarExclusionImages.append(exclusionsDict[x])
        except:
            pass


    #windExclusions = [exclusionsDict[x] for x in windExclusions]
    #solarExclusions = [exclusionsDict[x] for x in solarExclusions]
    windExclusionImages = compute_exclusions(windExclusionImages)
    solarExclusionImages = compute_exclusions(solarExclusionImages)
    windPotential = windPowerRaster()
    solarPotential = solarPowerRaster()
    localWind = windPotential.multiply(windExclusionImages).reduceRegion(ee.Reducer.sum(), activeGeom).getInfo()
    localSolar = solarPotential.multiply(solarExclusionImages).reduceRegion(ee.Reducer.sum(), activeGeom).getInfo()

    totalArea = usableAreaPerGeom(activeGeom, windPotential.gt(0).Or(solarPotential.gt(0)))

    testdict =  {"Development Area": totalArea, "Solar Potential": localSolar, "Wind Potential": localWind}#jsonify(DevelopmentArea = totalArea, SolarPotential = localSolar, windPotential = localWind)
    return testdict
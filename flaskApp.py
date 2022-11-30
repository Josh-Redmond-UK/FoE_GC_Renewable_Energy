from utils import *
from flask import Flask
from flask import jsonify
app = Flask(__name__)

@app.route('/<postcode>')
def renewablePotential(postcode):  
    ladGeometries = postcodeToGeom(postcode)

    activeGeom = postcodeToGeom(postcode, ladGeometries) ## Works with LAD only for near you page

    # Write utils default exclusions
    exclusionsDict = getExclusionsDict()
    windExclusions = getExclusions("common") + getExclusions("wind")
    solarExclusions = getExclusions("common") + getExclusions("solar")
    
    windExclusions = [exclusionsDict[x] for x in windExclusions]
    solarExclusions = [exclusionsDict[x] for x in solarExclusions]
    
    windPotential = windPowerRaster()
    solarPotential = solarPowerRaster()

    localWind = getPowerLocal(activeGeom, windExclusions, windPotential)
    localSolar = getPowerLocal(activeGeom, solarExclusions, solarPotential)
    totalArea = usableAreaPerGeom(activeGeom, windPotential.gt(0).Or(solarPotential.gt(0)))

    return jsonify(DevelopmentArea = totalArea, SolarPotential = localSolar, windPotential = localWind)

    
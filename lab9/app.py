from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import numpy as np
import rasterio
import geopandas as gpd

app = Flask(__name__)

cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'

file_path = '../dataset2/soil_moisture.tif'
with rasterio.open(file_path) as src:
    bbox = src.bounds

@app.route('/get_image_bbox')
def get_image_bbox():
    return jsonify({
        'lat_max': bbox.top,
        'lat_min': bbox.bottom,
        'lon_max': bbox.right,
        'lon_min': bbox.left
    })

@app.route('/get_moisture_value')
def get_moisture_value():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))

    if not (bbox.left <= lon <= bbox.right and bbox.bottom <= lat <= bbox.top):
        return jsonify({'moisture': 'no data'})

    with rasterio.open(file_path) as src:
        row, col = src.index(lon, lat)
        moisture = int(src.read(1, window=((row, row+1), (col, col+1))))

    return jsonify({'moisture': moisture})

if __name__ == '__main__':
    app.run(debug=True)
import numpy as np
import pandas as pd
import geopandas as gpd
import folium

from shapely.geometry import Point, Polygon
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier

from requests import Request
import requests
from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService
import os
import webbrowser
import openweathermapy as owm

def get_humanact(name):
    # URL for WFS backend
    url = "https://ows.emodnet-humanactivities.eu/wfs"

    # Initialize
    wfs = WebFeatureService(url=url)

    # Fetch the last available layer (as an example) --> 'vaestoruutu:vaki2021_5km'
    layer_name = name

    # Specify the parameters for fetching the data
    params = dict(service='WFS', version="2.0.0", request='GetFeature',
        typeName=layer_name, outputFormat='json')

    # Parse the URL with parameters
    wfs_request_url = Request('GET', url, params=params).prepare().url

    # Read data from URL
    gdf = gpd.read_file(wfs_request_url)

    return gdf

wind_farms = get_humanact("windfarms")
potential_areas = Point(1.7, 57)

def get_bathymetry(lat, lon):
    api_url = f"https://ows.emodnet-bathymetry.eu/wms?service=WMS&version=1.3.0&request=GetFeatureInfo&layers=mean_atlas_depth&query_layers=mean_atlas_depth&crs=EPSG:4326&styles=&bbox={lon-0.1},{lat-0.1},{lon+0.1},{lat+0.1}&width=101&height=101&format=image/png&info_format=text/plain&i=50&j=50"
    # send the API request and get the response
    response = requests.get(api_url)
    depth_str = response.text.split("Depth = ")[1].split(" ")[0]
    bathymetry_data = float(depth_str)
    return bathymetry_data

# def get_windspeed(lat, lon):
#     api_key = "11741b2d1a55e57d579f35fef71586db"
#     url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&appid={api_key}&units=metric'
#     response = requests.get(url)
#     response_json = response.json()
#     wind_speed = response_json['hourly'][0]['wind_speed']
#     return wind_speed

wind_speeds = []
elevation = []

for point in wind_farms.geometry:
    lat = point.y
    lon = point.x
    #wind_speeds.append(get_windspeed(lat, lon))
    elevation.append(get_bathymetry(lat, lon))

wind_farms['Wind Speed (kph)'] = wind_speeds

# Cluster the existing wind farms based on their geographical location and capacity
kmeans = KMeans(n_clusters=5)
kmeans.fit(wind_farms[['geometry', 'capacity']].to_numpy())

# Add the cluster labels as features for classification
wind_farms['cluster'] = kmeans.labels_

# Train a decision tree classifier on the wind farms data
X = wind_farms[['geometry', 'capacity', 'cluster']]
y = wind_farms['suitable']
clf = DecisionTreeClassifier()
clf.fit(X.to_numpy(), y.to_numpy())

# Use the trained classifier to predict suitable areas for wind farm placement
X_new = potential_areas[['geometry', 'capacity']]
potential_areas['suitable'] = clf.predict(X_new.to_numpy())

# Save the results to a shapefile
potential_areas.to_file('suitable_areas.shp')
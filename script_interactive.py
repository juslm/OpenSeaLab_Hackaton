import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from folium.plugins import MousePosition
from shapely.geometry import Polygon
from shapely.geometry import Point

from requests import Request
import requests
from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService
import os
import webbrowser
import urllib.parse

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

xmin = -30
xmax = 40
ymin = 28
ymax = 73

munitions_buffer = 5000
platforms_buffer = 5000
windfarmspoly_buffer = 0

min_speed = 4
max_speed = 15

windspeeds = pd.read_csv("data/windspeeds.csv", names = ["geometry", "speed(m/s)"])
windspeeds["geometry"] = [Point(eval(s)) for s in windspeeds["geometry"]]
windspeeds["weight"] = [n/max(windspeeds["speed(m/s)"]) for n in windspeeds["speed(m/s)"]]
windspeeds = gpd.GeoDataFrame(windspeeds)

tiles = []

dist = abs(windspeeds.geometry[0].xy[1][0]-windspeeds.geometry[1].xy[1][0])

for i, point in enumerate(windspeeds.geometry):
    x = point.xy[0][0]
    y = point.xy[1][0]
    tiles.append(Polygon([[x-dist/2, y+dist/2], [x+dist/2, y+dist/2], [x+dist/2, y-dist/2], [x-dist/2, y-dist/2]]))

windspeeds["tiles"] = gpd.GeoSeries(tiles, crs = "EPSG:4326")

data = ["munitions", "platforms", "windfarmspoly"]
buffers = {}

buffers["munitions"] = munitions_buffer
buffers["platforms"] = platforms_buffer
buffers["windfarmspoly"] = windfarmspoly_buffer

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

coordinates = world["geometry"]

water = gpd.GeoSeries(Polygon([[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]), crs = 4326).difference(world.geometry.unary_union)
safe = water.to_crs("EPSG:32634")

colors = ['red', 'purple', 'blue', 'yellow']

m = folium.Map(zoom_start = 5, location = [51.505, -0.09], control_scale = True)

jsons = {}

for i, layer in enumerate(data):
    ha = get_humanact(layer).to_crs("EPSG:4326")
    ha["layer"] = pd.Series([layer for x in range(len(ha.index))])
    ha.explore(m=m, color=colors[i], name=layer, show = False)
    circles = ha.to_crs("EPSG:32634").geometry.buffer(buffers[layer])
    mp = circles.unary_union
    safe = safe.difference(mp)
    jsons[layer] = ha.to_json()

safe = gpd.GeoDataFrame(geometry = safe)
safe.explode()

folium.GeoJson(data=safe.geometry, style_function=lambda x:{"fillColor":"green", "color":"green"}, name = "safe").add_to(m)

w = folium.FeatureGroup(name='wind speed').add_to(m)
for i, row in windspeeds.iterrows():
    if min_speed < row["speed(m/s)"] < max_speed and not any(row["tiles"].intersects(world.geometry)):
        b = folium.GeoJson(data=row["tiles"], style_function=lambda x:{"fillColor":"white", "color":"black"})
        b.add_child(folium.Popup(str(row["speed(m/s)"])))
        w.add_child(b)

folium.LayerControl().add_to(m)
MousePosition().add_to(m)

jsons["safe"] = safe.to_json()

m.save('my_map.html')
webbrowser.open('file://' + os.path.realpath('my_map.html'))
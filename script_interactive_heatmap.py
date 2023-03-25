import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry import Polygon
import folium
from folium.plugins import HeatMap

from requests import Request
from owslib.wfs import WebFeatureService
import urllib.parse
import os
import webbrowser

def get_humanact(name):
    # URL for WFS backend
    url = "https://ows.emodnet-humanactivities.eu/wfs"

    # Initialize
    wfs = WebFeatureService(url=url)

    # Fetch the last available layer (as an example) --> 'vaestoruutu:vaki2021_5km'
    layer_name = name

    # Specify the parameters for fetching the data
    # Count: specificies amount of rows to return (e.g. 10000 or 100)
    # startIndex: specifies at which offset to start returning rows
    params = dict(service='WFS', version="2.0.0", request='GetFeature',
        typeName=layer_name, outputFormat='json')

    # Parse the URL with parameters
    wfs_request_url = Request('GET', url, params=params).prepare().url

    # Read data from URL
    gdf = gpd.read_file(wfs_request_url)

    return gdf

points_data = ["munitions", "platforms"]
polygons_data = ["platforms", "windfarmspoly"]

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
coord = [50, 0]

m = folium.Map(zoom_start = 5, location = coord)
color = []

for i, layer in enumerate(points_data):
    ha = get_humanact(layer)
    ha["layer"] = pd.Series([layer for x in range(len(ha.index))])
    heat_data = [[point.xy[1][0], point.xy[0][0]] for point in ha.geometry]
    HeatMap(heat_data, name = layer, max_zoom = 2, blur = 0).add_to(m)

folium.LayerControl().add_to(m)

m.save('my_map.html')
webbrowser.open('file://' + os.path.realpath('my_map.html'))
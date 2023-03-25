import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap

from requests import Request
import requests
from owslib.wfs import WebFeatureService
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
    params = dict(service='WFS', version="2.0.0", request='GetFeature',
        typeName=layer_name, outputFormat='json')

    # Parse the URL with parameters
    wfs_request_url = Request('GET', url, params=params).prepare().url

    # Read data from URL
    gdf = gpd.read_file(wfs_request_url)

    return gdf

points_data = ["munitions", "platforms", "heritageshipwrecks"]
poly_data = ["windfarmspoly"]

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world_poly = world.geometry.unary_union

colors = ['red', 'green', 'blue', 'yellow']

m = folium.Map(zoom_start = 5, location = [51.505, -0.09])

for i, layer in enumerate(points_data):
    ha = get_humanact(layer).to_crs("EPSG:4326")
    ha["layer"] = pd.Series([layer for x in range(len(ha.index))])
    heat_data = [[point.xy[1][0], point.xy[0][0]] for point in ha.geometry]
    heatmap = HeatMap(heat_data, name = layer, gradient={0:"white", 1:colors[i]}, radius = 10, max_zoom = 1, blur = 5)
    # Add the density map to the map
    heatmap.add_to(m)

for j, layer in enumerate(poly_data):
    ha = get_humanact(layer).to_crs("EPSG:4326")
    ha["layer"] = pd.Series([layer for x in range(len(ha.index))])
    ha.explore(
     m=m,
     color=colors[i+1+j],
     name=layer
    )

folium.LayerControl().add_to(m)

m.save('my_map.html')
webbrowser.open('file://' + os.path.realpath('my_map.html'))
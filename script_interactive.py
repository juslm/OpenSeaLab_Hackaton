import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import HeatMap
from shapely.geometry import Polygon

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

points_data = ["munitions", "platforms"]
poly_data = ["windfarmspoly"]

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

coordinates = world["geometry"]

xmin = -30
xmax = 55
ymin = 28
ymax = 73

safe = gpd.GeoSeries(Polygon([[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]), crs = 4326).difference(world.geometry.unary_union)
safe = safe.to_crs("EPSG:32634")

colors = ['red', 'purple', 'blue', 'yellow']

m = folium.Map(zoom_start = 5, location = [51.505, -0.09])

for i, layer in enumerate(points_data):
    ha = get_humanact(layer).to_crs("EPSG:4326")
    ha["layer"] = pd.Series([layer for x in range(len(ha.index))])
    ha.explore(
     m=m,
     color=colors[i],
     name=layer
    )
    circles = ha.to_crs("EPSG:32634").geometry.buffer(1000)
    mp = circles.unary_union
    safe = safe.difference(mp)

for j, layer in enumerate(poly_data):
    ha = get_humanact(layer).to_crs("EPSG:4326")
    ha["layer"] = pd.Series([layer for x in range(len(ha.index))])
    ha.explore(
     m=m,
     color=colors[i+1+j],
     name=layer
    )
    circles = ha.to_crs("EPSG:32634").geometry
    mp = circles.unary_union
    safe = safe.difference(mp)

folium.LayerControl().add_to(m)

safe = gpd.GeoDataFrame(geometry = safe)
safe.explode()

folium.GeoJson(data=safe.geometry).add_to(m)

m.save('my_map.html')
webbrowser.open('file://' + os.path.realpath('my_map.html'))
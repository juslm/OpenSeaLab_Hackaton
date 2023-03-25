import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry import Polygon
import folium

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

def get_physics(name):
    # URL for WFS backend
    url = "https://prod-geoserver.emodnet-physics.eu/geoserver/EMODnet/ows"

    # Initialize
    wfs = WebFeatureService(url=url)

    # Fetch the last available layer (as an example) --> 'vaestoruutu:vaki2021_5km'
    layer_name = name

    # Specify the parameters for fetching the data
    # Count: specificies amount of rows to return (e.g. 10000 or 100)
    # startIndex: specifies at which offset to start returning rows
    params = dict(service='WFS', version="1.0.0", request='GetFeature',
        typeName=layer_name, outputFormat='json')

    # Parse the URL with parameters
    wfs_request_url = urllib.parse.unquote(Request('GET', url, params=params).prepare().url)

    # Read data from URL
    gdf = gpd.read_file(wfs_request_url)

    return gdf

#wind = get_physics("EMODnet%3ADAT_LatestDataParametersProduct")

layers = ["munitions", "platforms", "heritageshipwrecks", "windfarmspoly"]
buffers = [4000, 3000, 1000, 3000]

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world_poly = world.geometry.unary_union

buffer_dict = {}
all_layers = pd.DataFrame()

colors = ['red', 'green', 'blue', 'yellow']

m = folium.Map()

for i, layer in enumerate(layers):
    ha = get_humanact(layer).to_crs("EPSG:32634")
    ha["layer"] = pd.Series([layer for x in range(len(ha.index))])
    ha.geometry = ha.geometry.buffer(buffers[i])
    ha.explore(
     m=m,
     color=colors[i],
     name=layer
    )

folium.TileLayer('Stamen Toner', control=True).add_to(m)  # use folium to add alternative tiles
folium.LayerControl().add_to(m)

m.save('my_map.html')
webbrowser.open('file://' + os.path.realpath('my_map.html'))
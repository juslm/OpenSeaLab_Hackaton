import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point
from shapely.geometry import Polygon

from requests import Request
from owslib.wfs import WebFeatureService

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

layers = ["munitions", "platforms", "heritageshipwrecks", "windfarmspoly"]

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

fig, ax = plt.subplots(figsize=(10, 10))

colors = ['r', 'g', 'b', 'k', 'y']

coordinates = world["geometry"]

xmin = -30
xmax = 55
ymin = 28
ymax = 73

safe = gpd.GeoSeries(Polygon([[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]), crs = 4326).difference(world["geometry"].unary_union)

data_dict = {}

for i, layer in enumerate(layers):
    ha = get_humanact(layer)
    data_dict[layer] = ha
    circles = ha["geometry"].buffer(0.1)
    mp = circles.unary_union
    safe = safe.difference(mp)

safe.plot(ax=ax, color = "green")
ax.set_facecolor('xkcd:salmon')
ax.set_facecolor((1.0, 0.47, 0.42))
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)

plt.show()
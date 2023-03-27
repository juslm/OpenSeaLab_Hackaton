from .get_humanact import get_humanact
import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from shapely.geometry import Point


def get_munitions(name="munitions"):
    ha = get_humanact(name).to_crs("EPSG:4326")
    return ha.to_json()


def get_platforms(name="platforms"):
    ha = get_humanact(name).to_crs("EPSG:4326")
    return ha.to_json()


def get_windfarmspoly(name="windfarmspoly"):
    ha = get_humanact(name).to_crs("EPSG:4326")
    return ha.to_json()


def get_safe(xmin=-30,
             xmax=40,
             ymin=28,
             ymax=73,
             munitions_buffer=5000,
             platforms_buffer=5000,
             windfarmspoly_buffer=0,
             data=None):
    if data is None:
        data = ["munitions", "platforms", "windfarmspoly"]
    buffers = {"munitions": munitions_buffer, "platforms": platforms_buffer, "windfarmspoly": windfarmspoly_buffer}

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    water = gpd.GeoSeries(Polygon([[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]), crs=4326).difference(
        world.geometry.unary_union)
    safe = water.to_crs("EPSG:32634")

    for i, layer in enumerate(data):
        ha = get_humanact(layer).to_crs("EPSG:4326")
        ha["layer"] = pd.Series([layer for x in range(len(ha.index))])
        circles = ha.to_crs("EPSG:32634").geometry.buffer(buffers[layer])
        mp = circles.unary_union
        safe = safe.difference(mp)

    safe = gpd.GeoDataFrame(geometry=safe)
    safe.explode()

    return safe.to_json()

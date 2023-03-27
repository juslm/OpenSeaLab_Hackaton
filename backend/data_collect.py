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


def get_windspeedgrid(min_speed=4, max_speed=15):
    windspeeds = pd.read_csv("../data/windspeeds.csv", names=["geometry", "speed(m/s)"])
    windspeeds["geometry"] = [Point(eval(s)) for s in windspeeds["geometry"]]
    windspeeds["weight"] = [n / max(windspeeds["speed(m/s)"]) for n in windspeeds["speed(m/s)"]]
    windspeeds = gpd.GeoDataFrame(windspeeds)

    tiles = []

    dist = abs(windspeeds.geometry[0].xy[1][0] - windspeeds.geometry[1].xy[1][0])

    for i, point in enumerate(windspeeds.geometry):
        x = point.xy[0][0]
        y = point.xy[1][0]
        tiles.append(Polygon([[x - dist / 2, y + dist / 2], [x + dist / 2, y + dist / 2], [x + dist / 2, y - dist / 2],
                              [x - dist / 2, y - dist / 2]]))

    windspeeds["tiles"] = gpd.GeoSeries(tiles, crs="EPSG:4326")
    windspeeds = windspeeds[
        (min_speed <= windspeeds["speed(m/s)"]) & (max_speed >= windspeeds["speed(m/s)"])].reset_index()
    print(windspeeds)
    return [windspeeds.to_json(), windspeeds]


def get_safe(munitions_buffer=5000,
             platforms_buffer=5000,
             windfarmspoly_buffer=0,
             data=None):
    if data is None:
        data = ["munitions", "platforms", "windfarmspoly"]
    buffers = {"munitions": munitions_buffer, "platforms": platforms_buffer, "windfarmspoly": windfarmspoly_buffer}

    windspeeds = get_windspeedgrid()[1]

    safe = windspeeds["tiles"].to_crs("EPSG:32634")
    safe = safe.unary_union

    for i, layer in enumerate(data):
        ha = get_humanact(layer).to_crs("EPSG:4326")
        circles = ha.to_crs("EPSG:32634").geometry.buffer(buffers[layer])
        mp = circles.unary_union
        safe = safe.difference(mp)

    safe = gpd.GeoDataFrame(geometry=gpd.GeoSeries(safe), crs="EPSG:32634")

    return safe.to_json()

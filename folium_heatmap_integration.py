# Make sure to run generate_depth_small_dataset.py!!!


import numpy as np
import pandas as pd
import geopandas as gpd
import folium
from folium import plugins
from folium import raster_layers
from folium.plugins import HeatMap
from folium.plugins import MousePosition
from shapely.geometry import Polygon
from shapely.geometry import Point
from requests import Request
import requests
from owslib.wfs import WebFeatureService
from owslib.wms import WebMapService
import os
from branca.element import Template, MacroElement
import urllib.parse
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

windspeeds["geometry"] = gpd.GeoSeries(tiles, crs = "EPSG:4326")

rest_wind = windspeeds[(min_speed >= windspeeds["speed(m/s)"]) | (max_speed <= windspeeds["speed(m/s)"])].reset_index()
windspeeds = windspeeds[(min_speed <= windspeeds["speed(m/s)"]) & (max_speed >= windspeeds["speed(m/s)"])].reset_index()

data = ["munitions", "platforms", "windfarmspoly"]
buffers = {}

buffers["munitions"] = munitions_buffer
buffers["platforms"] = platforms_buffer
buffers["windfarmspoly"] = windfarmspoly_buffer

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

coordinates = world["geometry"]

#water = gpd.GeoSeries(Polygon([[xmin, ymin], [xmin, ymax], [xmax, ymax], [xmax, ymin]]), crs = 4326).difference(world.geometry.unary_union)
#safe = water.to_crs("EPSG:32634")

colors = ['red', 'purple', 'blue', 'yellow']

m = folium.Map(zoom_start = 5, location = [51.505, -0.09], control_scale = True)

safe = windspeeds["geometry"].to_crs("EPSG:32634")
safe = safe.unary_union

for i, layer in enumerate(data):
    ha = get_humanact(layer).to_crs("EPSG:4326")
    ha["layer"] = pd.Series([layer for x in range(len(ha.index))])
    ha.explore(m=m, color=colors[i], name=layer, show = True)
    circles = ha.to_crs("EPSG:32634").geometry.buffer(buffers[layer])
    mp = circles.unary_union
    safe = safe.difference(mp)

# safe = safe.difference(gpd.GeoSeries(windspeeds["tiles"].to_crs("EPSG:32634").unary_union, crs = "EPSG:32634"))
safe = gpd.GeoDataFrame(geometry = gpd.GeoSeries(safe), crs = "EPSG:32634")

folium.GeoJson(data=safe.geometry, style_function=lambda x:{"fillColor":"green", "color":"green"}, name = "safe").add_to(m)

w = folium.FeatureGroup(name='wind speed',show=False).add_to(m)
for i, row in windspeeds.iterrows():
    b = folium.GeoJson(data=row["geometry"], style_function=lambda x:{"fillColor":"white", "color":"black"})
    b.add_child(folium.Popup(str(row["speed(m/s)"])))
    w.add_child(b)

# heatmap integration


file=open('data/depth_small.txt','r')
depth=pd.read_table(file,delimiter=';',names=['long', 'lat', 'depth'])

df_folium = pd.DataFrame({'Lat':depth['lat'],'Long':depth['long'],'Depth':depth['depth']})

df_folium['weight'] = df_folium['Depth'] / df_folium['Depth'].min()

# heatmap based on weight

map_values1 = df_folium[['Lat','Long','weight']]

data = map_values1.values.tolist()


heatmap_fg=folium.FeatureGroup(name='Depth', show=True).add_to(m)
hm = HeatMap(data, gradient={0.08: 'darkblue', 0.2: 'lime', 0.5: 'yellow', 0.7: 'orange', 1: 'red'},
                min_opacity=0.12, 
                max_opacity=0.9, 
                radius=10,
                use_local_extrema=False)#.add_to(base_map)
heatmap_fg.add_child(hm)


template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:14px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Depth(m) (Draggable 0_o)</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:blue;opacity:0.7;'></span>0-500</li>
    <li><span style='background:lime;opacity:0.7;'></span>500-1300</li>
    <li><span style='background:yellow;opacity:0.7;'></span>1300-3200</li>
    <li><span style='background:orange;opacity:0.7;'></span>3200-4500</li>
    <li><span style='background:red;opacity:0.7;'></span>4500-6500</li>

  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 18px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 16px;
    width: 30px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""

macro = MacroElement()
macro._template = Template(template)
heatmap_fg.add_child(macro)















folium.LayerControl().add_to(m)
MousePosition().add_to(m)
m.save('my_map.html')
webbrowser.open('file://' + os.path.realpath('my_map.html'))

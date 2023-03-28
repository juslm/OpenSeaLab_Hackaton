import numpy as np
import pandas as pd
import geopandas as gpd
import folium
import rasterio
from folium import plugins
from folium import raster_layers
from folium.plugins import HeatMap
from folium.plugins import MousePosition
from shapely.geometry import Polygon
import os
import webbrowser
from branca.element import Template, MacroElement

file=open('data/depth_small.txt','r')
depth=pd.read_table(file,delimiter=';',names=['long', 'lat', 'depth'])

df_folium = pd.DataFrame({'Lat':depth['lat'],'Long':depth['long'],'Depth':depth['depth']})

df_folium['weight'] = df_folium['Depth'] / df_folium['Depth'].min()

# heatmap based on weight


def generateBaseMap(loc, zoom=4, tiles='OpenStreetMap', crs='ESPG2263'):
    return folium.Map(location=loc,
                   control_scale=True, 
                   zoom_start=zoom,
                   tiles=tiles)
  
base_map = generateBaseMap([40, 0] )

map_values1 = df_folium[['Lat','Long','weight']]

data = map_values1.values.tolist()
           
hm = HeatMap(data, gradient={0.08: 'darkblue', 0.2: 'lime', 0.5: 'yellow', 0.7: 'orange', 1: 'red'},
                min_opacity=0.12, 
                max_opacity=0.9, 
                radius=10,
                use_local_extrema=False)#.add_to(base_map)

base_map.add_child(hm)


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
base_map.get_root().add_child(macro)




MousePosition().add_to(base_map)

folium.LayerControl().add_to(base_map)
base_map.save('depth_heatmap.html')
webbrowser.open('file://' + os.path.realpath('depth_heatmap.html'))

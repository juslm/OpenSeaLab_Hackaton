from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv

 
m =io.imread(r"data/vessel_density.png")
# Set the initial coordenates of the map
north = 86.842727
south = 14.961111
east = 97.633027
west = -87.706484

np_image = np.array(m)
# Set the size of the image
width = 867
heigth = 962

relation_ew=(east-west)/width
relation_ns=(north-south)/heigth

list = []

for j, column in enumerate(m):
    for i, rgb in enumerate(column):
        point = "POINT("+str(east-relation_ew*(j+1))+","+str(north-relation_ns*(i+1))+")"
        list.append([point, rgb])

df = pd.DataFrame(list, columns = ["geometry", "rgb"])

df.to_csv("data/vessel_rgb.csv")

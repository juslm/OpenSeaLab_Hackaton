from skimage import io
import matplotlib.pyplot as plt
import numpy as np

 
m =io.imread(r"C:\Users\Diego\Desktop\Gante\hackathon\map_png.png")
print("Dimensiones de la imagen:")
print(m.shape)
plt.imshow(m,vmin=0,vmax=1)
# Set the initial coordenates of the map
north = 86.842727
south = 14.961111
east = 97.633027
west = -87.706484

np_image = np.array(m)
# Set the size of the image
width = 962
heigth = 867

relation_ew=(east-west)/width
relation_ns=(north-south)/heigth
print(relation_ew, relation_ns)
print(width, heigth, len(m))
print(m[0])
coordenates={}
counter=0
counter2=0
y=0
print(m)
# for j, column in enumerate(m):
#     coordenates[tuple([north,(east-x*relation_ew)])]=m[x][y]
#     for y in x:
#         if x ==0 and y==0:
#             coordenates[tuple([north,west])]=m[x][y]
#         elif x==0 and (north-y*relation_ns)==len(m):
#             coordenates[tuple([south,west])]=m[x][y]
#         else:
#             coordenates[tuple([(north-y*relation_ns),(east-x*relation_ew)])]=m[x][y]

print(962*867-len(coordenates.keys()))



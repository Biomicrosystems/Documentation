import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

d = float(raw_input('distancia al sensor (cm): '))
length = float(raw_input('largo del sistema (cm): '))
width = float(raw_input('ancho del sistema (cm): '))

x_angle = [-32.5, -23, -13.5, -4.5, 4.5, 13.5, 23, 32.5, -31, -22, -13, -4, 4, 13, 22, 31, -30, -21, -12.5, -4, 4, 12.5, 21, 30, -29, -21, -12, -4, 4, 12, 21, 29, -29, -21, -12, -4, 4, 12, 21, 29, -30, -21, -12.5, -4, 4, 12.5, 21, 30, -31, -22, -13, -4, 4, 13, 22, 31, -32.5, -23, -13.5, -4.5, 4.5, 13.5, 23, 32.5]

x_angle_radians = []
for x in x_angle:
	x_angle_radians.append(x*math.pi/180)

y_angle = [32.5, 31, 29, 28.5, 28.5, 29, 31, 32.5, 22.5, 22, 21, 20.5, 20.5, 21, 22, 22.5, 13.5, 13, 12.5, 12, 12, 12.5, 13, 13.5, 4.5, 4, 4, 4, 4, 4, 4, 4.5, -4.5, -4, -4, -4, -4, -4, -4, -4.5, -13.5, -13, -12.5, -12, -12, -12.5, -13, -13.5, -22.5, -22, -21, -20.5, -20.5, -21, -22, -22.5, -32.5, -31, -29, -28.5, -28.5, -29, -31, -32.5]

y_angle_radians = []
for y in y_angle:
	y_angle_radians.append(y*math.pi/180)

x_distance = []
for x in x_angle_radians:
	x_distance.append(d*math.tan(x))
y_distance = []
for y in y_angle_radians:
	y_distance.append(d*math.tan(y))
	
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
rects  = [[[-1*length/2, -1*width/2, -0.1], [length/2, -1*width/2, -0.1], [length/2, width/2, -0.1], [-1*length/2, width/2, -0.1 ]]]                                                                                                                                                                                                                                                                                             
ax.add_collection3d(Poly3DCollection(rects))

ax.scatter(0, 0, d, color='r', linewidth = 3, label = 'Sensor')
ax.scatter(x_distance, y_distance, 0, color = 'black', linewidth=1, label = 'Pixeles')

for i in range(0, len(x_distance)):
	ax.plot([0,x_distance[i]], [0,y_distance[i]], [d, 0], color='r', linewidth=0.2)

ax.set_zbound(lower=0, upper=d)
ax.legend()
plt.title('Puntos vistos por el sensor a \n' + str(d) + ' cm')
plt.xlabel('Distancias X')
plt.ylabel('Distancias Y')
plt.grid()
plt.show()



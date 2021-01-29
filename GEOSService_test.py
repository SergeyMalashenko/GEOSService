#!/usr/bin/env python3
import argparse
import json  
import math

import numpy as np
import scipy as sp

from matplotlib       import pyplot
from shapely.geometry import LineString
from descartes        import PolygonPatch

from GEOSService_common import SIZE, BLUE, GRAY, GREEN, RED, set_limits 
from GEOSService_common import plot_line, plot_coords


def plot_coords(ax, x, y, color='#999999', zorder=1):
    ax.plot(x, y, 'o', color=color, zorder=zorder)

with open('data/os.json.log') as json_file:
    data = json.load(json_file)

point_s_s = list()
for key_i, value_i in data.items():
    if key_i == 'axis':
        for key_j, value_j in value_i.items():
            if key_j == 'lines':
                for line in value_j:
                    for key_k, value_k in line.items():
                        if key_k == 'points':
                            point_s = [ (float(point['x']),float(point['y'])) for point in value_k ]
                            point_s_s.append( point_s )

x_min, x_max =  float("inf"), -float("inf")
y_min, y_max =  float("inf"), -float("inf")

fig, ax = pyplot.subplots(1, figsize=(2*SIZE[0], 2 * SIZE[1]), dpi=90)
for point_s in point_s_s:
    line = LineString(point_s)
    bounds = line.bounds
    x_min, x_max = min( bounds[0], x_min ), max( bounds[2], x_max )
    y_min, y_max = min( bounds[1], y_min ), max( bounds[3], y_max )
    
x_length = x_max - x_min 
y_length = y_max - y_min
ax.set_xlim(math.floor(x_min - x_length*0.1), math.ceil(x_max + x_length*0.1))
ax.set_ylim(math.floor(y_min - y_length*0.1), math.ceil(y_max + y_length*0.1))
ax.set_aspect("equal")
'''
for point_s in point_s_s:
    line = LineString(point_s)
    x, y = list(line.coords)[0]
    buffer_ = line.buffer(10)
    
    patch1 = PolygonPatch(buffer_, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2)
    ax.add_patch(patch1)

    plot_line(ax, line)
    plot_coords(ax, x, y)
    simple_ = buffer_.simplify(tolerance=1)
    x, y = buffer_.exterior.coords.xy
    #plot_coords(ax, x, y)
    x, y = simple_.exterior.coords.xy
    plot_coords(ax, x, y)


    # Turn off tick labels
    ax.set_yticklabels([])
    ax.set_xticklabels([])
'''

point_s = [item for sublist in point_s_s for item in sublist]
line = LineString(point_s)
x, y = list(line.coords)[0]
buffer_ = line.buffer(10)
    
patch1 = PolygonPatch(buffer_, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2)
ax.add_patch(patch1)

plot_line(ax, line)
#plot_coords(ax, x, y)
simple_ = buffer_.simplify(tolerance=1)
x, y = buffer_.exterior.coords.xy
#plot_coords(ax, x, y)
x, y = simple_.exterior.coords.xy
plot_coords(ax, x, y)
x, y = simple_.interiors[0].coords.xy
plot_coords(ax, x, y)



# Turn off tick labels
ax.set_yticklabels([])
ax.set_xticklabels([])

pyplot.show()


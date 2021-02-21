#!/usr/bin/env python3
import argparse
import shapely
import json  
import math

import numpy as np
import scipy as sp

from matplotlib       import pyplot

from shapely.geometry import LineString, LinearRing, Point, Polygon, MultiPolygon
from shapely.ops      import unary_union, orient
from descartes        import PolygonPatch

from GEOSService_common import SIZE, BLUE, GRAY, GREEN, RED, set_limits 
from GEOSService_common import plot_line, plot_coords

from GEOSService_common import generateArea, calculatePolygonNormals

print( shapely.__file__ )

def plot_coords(ax, x_s, y_s, color='#999999', zorder=1):
    ax.plot(x_s, y_s, 'o', color=color, zorder=zorder)
    for i, xy in enumerate(zip(x_s, y_s)):
        ax.annotate( f'{i}', xy=xy, textcoords='data')

def plot_line(ax, ob, color=GRAY):
    parts = hasattr(ob, 'geoms') and ob or [ob]
    for part in parts:
        x, y = part.xy
        ax.plot(x, y, color=color, linewidth=3, solid_capstyle='round', zorder=1)

with open('data/example_5.json') as json_file:
    data = json.load(json_file)

line_cap_style_  = data['cap_style'  ]
line_join_style_ = data['join_style' ]
polygon_join_style_ = 2 

resolution_ = data['resolution' ]
tolerance_  = data['tolerance'  ]
mitre_limit_= data['mitre_limit']
    
polygon_s          = list()
polygon_distance_s = list()
if 'polygons' in data:
    for polygon in data['polygons']:
        polygon_s         .append( polygon['points'  ] )
        polygon_distance_s.append( polygon['distance'] )

line_s          = list()
line_distance_s = list()
if 'lines' in data:
    for line in data['lines']:
        line_s         .append( line['points'  ] )
        line_distance_s.append( line['distance'] )

resultPolygon_s, basePolygon_s = generateArea( polygon_s, polygon_distance_s, polygon_join_style_, line_s, line_distance_s, line_cap_style_, line_join_style_, mitre_limit_, resolution_, tolerance_)
resultNormals_s = calculatePolygonNormals( resultPolygon_s )
baseNormals_s   = calculatePolygonNormals( basePolygon_s   )

x_min, y_min, x_max, y_max = resultPolygon_s.bounds
x_length = x_max - x_min
y_length = y_max - y_min

#Plot results
fig, ax = pyplot.subplots(1, figsize=(2*SIZE[0], 2 * SIZE[1]), dpi=90)
"""
ax.set_xlim(math.floor(x_min - x_length*0.1), math.ceil(x_max + x_length*0.1))
ax.set_ylim(math.floor(y_min - y_length*0.1), math.ceil(y_max + y_length*0.1))
"""
ax.set_aspect("equal")

for polygon in polygon_s:
    sourceLinearRing = LinearRing(polygon)
    x_s, y_s = ( [x for x, y in list (sourceLinearRing.coords)], [y for x, y in list (sourceLinearRing.coords)] )
    
    plot_coords(ax, x_s, y_s        , color=RED )
    plot_line  (ax, sourceLinearRing, color=RED )
for line in line_s:
    sourceLineString = LineString(line)
    x_s, y_s = ( [x for x, y in list (sourceLineString.coords)], [y for x, y in list (sourceLineString.coords)] ) 
    plot_coords(ax, x_s, y_s        , color=GREEN)
    plot_line  (ax, sourceLineString, color=GREEN)
for resultPolygon in resultPolygon_s:
    x_s, y_s = ( [x for x, y in list (resultPolygon.exterior.coords)], [y for x, y in list (resultPolygon.exterior.coords)] ) 
    plot_coords(ax, x_s, y_s, color=BLUE)
    
    patch2b = PolygonPatch(resultPolygon, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2)
    ax.add_patch(patch2b)

#Plot normal_s
for resultPolygon, resultNormals in zip(resultPolygon_s, resultNormals_s):
    xy_s = np.array([[x,y] for x, y in list (resultPolygon.exterior.coords)])
    n_s  = np.array([[x,y] for x, y in list (resultNormals.exterior.coords)])
    pyplot.quiver(xy_s[:,0], xy_s[:,1], n_s[:,0], n_s[:,1], angles='xy', scale_units='xy', scale=1./10)    

ax.set_title(f'cap_style={line_cap_style_}, join_style={line_join_style_}, mitre_limit={mitre_limit_}, resolution={resolution_}, tolerance={tolerance_}')
 
ax.set_yticklabels([])
ax.set_xticklabels([])
pyplot.show()


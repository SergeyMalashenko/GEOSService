from shapely.geometry import LineString, LinearRing, Point, Polygon, MultiPolygon
from shapely.ops      import unary_union, orient
from shapely          import affinity

from math import sqrt

import numpy as np

from numpy.linalg import norm

GM = (sqrt(5)-1.0)/2.0
W = 8.0
H = W*GM
SIZE = (W, H)

BLUE = '#6699cc'
GRAY = '#999999'
DARKGRAY = '#333333'
YELLOW = '#ffcc33'
GREEN = '#339933'
RED = '#ff3333'
BLACK = '#000000'

COLOR_ISVALID = {
    True: BLUE,
    False: RED,
}

def plot_line(ax, ob, color=GRAY, zorder=1, linewidth=3, alpha=1):
    x, y = ob.xy
    ax.plot(x, y, color=color, linewidth=linewidth, solid_capstyle='round', zorder=zorder, alpha=alpha)

def plot_coords(ax, ob, color=GRAY, zorder=1, alpha=1):
    x, y = ob.xy
    ax.plot(x, y, 'o', color=color, zorder=zorder, alpha=alpha)

def color_isvalid(ob, valid=BLUE, invalid=RED):
    if ob.is_valid:
        return valid
    else:
        return invalid

def color_issimple(ob, simple=BLUE, complex=YELLOW):
    if ob.is_simple:
        return simple
    else:
        return complex

def plot_line_isvalid(ax, ob, **kwargs):
    kwargs["color"] = color_isvalid(ob)
    plot_line(ax, ob, **kwargs)

def plot_line_issimple(ax, ob, **kwargs):
    kwargs["color"] = color_issimple(ob)
    plot_line(ax, ob, **kwargs)

def plot_bounds(ax, ob, zorder=1, alpha=1):
    x, y = zip(*list((p.x, p.y) for p in ob.boundary))
    ax.plot(x, y, 'o', color=BLACK, zorder=zorder, alpha=alpha)

def add_origin(ax, geom, origin):
    x, y = xy = affinity.interpret_origin(geom, origin, 2)
    ax.plot(x, y, 'o', color=GRAY, zorder=1)
    ax.annotate(str(xy), xy=xy, ha='center',
                textcoords='offset points', xytext=(0, 8))

def set_limits(ax, x0, xN, y0, yN):
    ax.set_xlim(x0, xN)
    ax.set_xticks(range(x0, xN+1))
    ax.set_ylim(y0, yN)
    ax.set_yticks(range(y0, yN+1))
    ax.set_aspect("equal")

def calculatePolygonNormals( inputPolygon_s ):
    def calculateNormals( point_s_list ):
        point_s_numpy  = np.array( point_s_list )
        
        normal_s_numpy_rht = np.roll(point_s_numpy, 1, axis=0) - point_s_numpy
        normal_s_numpy_lft = np.roll(point_s_numpy,-1, axis=0) - point_s_numpy
        
        normal_s_numpy_rht = np.roll(normal_s_numpy_rht, 1, axis=1)*np.array([[1,-1]])
        normal_s_numpy_lft = np.roll(normal_s_numpy_lft, 1, axis=1)*np.array([[-1,1]])
        normal_s_numpy = normal_s_numpy_rht / norm(normal_s_numpy_rht, axis=1, keepdims=True) + normal_s_numpy_lft / norm(normal_s_numpy_lft, axis=1, keepdims=True)
        normal_s_numpy = normal_s_numpy / norm(normal_s_numpy, axis=1, keepdims=True)
        
        return normal_s_numpy.tolist()

    outputPolygon_s = list()
    for inputPolygon in inputPolygon_s:
        #Process external points
        externalPoint_s   = list (inputPolygon.exterior.coords)
        externalPoint_s.pop()
        
        externalNormal_s = calculateNormals( externalPoint_s )
        
        internalNormal_s_s = list()
        for interior in inputPolygon.interiors:
            internalPoint_s = list (interior.coords)
            internalPoint_s.pop()
            
            internalNormal_s_s.append( calculateNormals(internalPoint_s) )
        outputPolygon_s.append( Polygon( externalNormal_s, holes=internalNormal_s_s ) )
    return MultiPolygon( outputPolygon_s  ) 


def generateArea( region_s, region_distance_s, region_join_style, line_s, line_distance_s, line_cap_style, line_join_style, mitre_limit=5, resolution=4, tolerance=0.05 ):
    resultPolygon_s = list()

    for region, distance in zip(region_s, region_distance_s):
        sourceLinearRing = LinearRing(region)
        sourcePolygon    = Polygon   (region)
        """ 
        if sourceLinearRing.is_ccw == False :
            targetLinearRing = sourceLinearRing.parallel_offset(distance, 'left' , resolution=resolution, join_style=region_join_style, mitre_limit=mitre_limit)
        if sourceLinearRing.is_ccw == True :
            targetLinearRing = sourceLinearRing.parallel_offset(distance, 'right', resolution=resolution, join_style=region_join_style, mitre_limit=mitre_limit)
        """
        targetLinearRing = sourcePolygon.buffer(distance, resolution=resolution, cap_style=1, join_style=region_join_style, mitre_limit=mitre_limit).exterior


        resultPolygon_s.append( Polygon(targetLinearRing ) )
    for line, distance in zip(line_s, line_distance_s, ):
        sourceLineString = LineString(line)
        targetLineString = sourceLineString.buffer(distance, resolution=resolution, cap_style=line_cap_style, join_style=line_join_style, mitre_limit=mitre_limit)
        resultPolygon_s.append( Polygon(targetLineString ) )
    
    unionPolygon_s = unary_union(resultPolygon_s)
    simplifiedPolygon_s = unionPolygon_s.simplify(tolerance, preserve_topology=False) 
    
    if simplifiedPolygon_s.geom_type == 'Polygon':
        simplifiedPolygon_s = MultiPolygon([simplifiedPolygon_s])
    
    return simplifiedPolygon_s, resultPolygon_s

def plotResults():
    return

#!/usr/bin/env python3
import argparse
import json  
import math
import os

import numpy as np
import scipy as sp

from GEOSService_common import generateArea

from flask      import Flask, request, jsonify
app = Flask(__name__)

ROOT_DIR   = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = 'output'

@app.route('/api/buffer', methods=['POST'])
def upload():
    resolution_ = request.json['resolution']
    tolerance_  = request.json['tolerance' ]
    
    axis_ = request.json['axis']
    
    region_s = list()
    for regions in axis_['regions']:
        for polygon in regions['polygons']:
            point_s = [ (float(point['x']),float(point['y'])) for point in polygon ]
            region_s.append( point_s )
    
    line_s   = list()
    for lines in axis_['lines']:
        point_s = [ (float(point['x']),float(point['y'])) for point in lines['points'] ]
        line_s.append( point_s )
    
    region_distance_s = [10]*len(region_s) 
    region_join_style = 2
    line_distance_s = [10]*len(line_s)
    line_cap_style = 1
    line_join_style = 1
    
    resultPolygon = generateArea( region_s, region_distance_s, region_join_style, line_s, line_distance_s, line_cap_style, line_join_style, resolution_, tolerance_)

    x_s, y_s = resultPolygon.exterior.coords.xy
    exterior_points = list( zip(x_s, y_s) )
    
    interior_points_s = list()
    for interior in resultPolygon.interiors:
        x_s, y_s = interior.coords.xy
        interior_points_s.append( list( zip(x_s,y_s) )  ) 
    
    return jsonify({'exterior_points':exterior_points, 'interior_points':interior_points_s})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

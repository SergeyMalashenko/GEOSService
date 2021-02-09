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
    line_cap_style_  = request.json['cap_style'  ]
    line_join_style_ = request.json['join_style' ]
    polygon_join_style_ = 2

    resolution_ = request.json['resolution' ]
    tolerance_  = request.json['tolerance'  ]
    mitre_limit_= request.json['mitre_limit']
    
    polygon_s          = list()
    polygon_distance_s = list()
    if 'polygons' in request.json:
        for polygon in request.json['polygons']:
            polygon_s         .append( polygon['points'  ] )
            polygon_distance_s.append( polygon['distance'] )
    
    line_s          = list()
    line_distance_s = list()
    if 'lines' in request.json:
        for line in request.json['lines']:
            line_s         .append( line['points'  ] )
            line_distance_s.append( line['distance'] )
    
    resultPolygon = generateArea( polygon_s, polygon_distance_s, polygon_join_style_, line_s, line_distance_s, line_cap_style_, line_join_style_, mitre_limit_, resolution_, tolerance_)

    x_s, y_s = resultPolygon.exterior.coords.xy
    exterior_points = list( zip(x_s, y_s) )
    
    interior_points_s = list()
    for interior in resultPolygon.interiors:
        x_s, y_s = interior.coords.xy
        interior_points_s.append( list( zip(x_s,y_s) )  ) 
    
    return jsonify({'exterior_points':exterior_points, 'interior_points':interior_points_s})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

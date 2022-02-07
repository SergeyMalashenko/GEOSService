#!/usr/bin/env python3
import argparse
import json  
import math
import os

import numpy as np
import scipy as sp

from GEOSService_common import generateArea, calculatePolygonNormals

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
    
    resultPolygon_s, basePolygon_s = generateArea( polygon_s, polygon_distance_s, polygon_join_style_, line_s, line_distance_s, line_cap_style_, line_join_style_, mitre_limit_, resolution_, tolerance_)
    resultNormals_s = calculatePolygonNormals(resultPolygon_s)
    baseNormals_s   = calculatePolygonNormals(basePolygon_s  )
   
    resultPoints_s = list()
    for resultPolygon, resultNormals in zip(resultPolygon_s, resultNormals_s):
        point_x_s , point_y_s  = resultPolygon.exterior.coords.xy
        normal_x_s, normal_y_s = resultNormals.exterior.coords.xy
        
        exterior_points  = list( zip(point_x_s , point_y_s ) )
        exterior_normals = list( zip(normal_x_s, normal_y_s) )
        
        interior_points_s  = list()
        interior_normals_s = list()
        for Points, Normals in zip( resultPolygon.interiors, resultNormals.interiors ):
            point_x_s , point_y_s  = Points .coords.xy
            normal_x_s, normal_y_s = Normals.coords.xy
            interior_points_s .append( list( zip(point_x_s , point_y_s ) ) ) 
            interior_normals_s.append( list( zip(normal_x_s, normal_y_s) ) ) 
        resultPoints_s.append( {
            'exterior_points':exterior_points, 'interior_points':interior_points_s,
            'exterior_normals':exterior_normals,'interior_normals':interior_normals_s,
            'area':resultPolygon.area
        } )
    return jsonify(resultPoints_s)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

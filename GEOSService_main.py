#!/usr/bin/env python3
import argparse
import json  
import math
import os

import numpy as np
import scipy as sp

from matplotlib       import pyplot
from shapely.geometry import LineString
from descartes        import PolygonPatch

from flask      import Flask, request, jsonify
app = Flask(__name__)

ROOT_DIR   = os.path.abspath(os.path.dirname(__file__))
OUTPUT_DIR = 'output'

@app.route('/api/buffer', methods=['POST'])
def upload():
    tolerance = request.json['tolerance']
    distance  = request.json['distance' ]
    points    = request.json['points'   ]
    style     = request.json['style'    ]
    
    print('Hello world!')
    
    line_   = LineString(points)
    buffer_ = line_.buffer(distance, cap_style=1, join_style=1)
    simple_ = buffer_.simplify(tolerance=tolerance)
    
    exterior_points = list()
    x_s, y_s = simple_.exterior.coords.xy
    for (x,y) in zip(x_s, y_s):
        exterior_points.append( (x,y) )
    
    interior_points_s = list()
    for interior in simple_.interiors:
        interior_points = list()
        x_s, y_s = interior.coords.xy
        for (x,y) in zip(x_s, y_s):
            interior_points.append( (x,y) )
        interior_points_s.append( interior_points )
    
    return jsonify({'exterior_points':exterior_points, 'interior_points':interior_points_s})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

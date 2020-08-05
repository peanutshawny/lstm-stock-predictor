'''server/app.py - main api app declaration'''
import time
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)

##
# API routes
##

@app.route('/api/items')
def items():
  '''Sample API route for data'''
  return jsonify([{'title': 'Shawn'}, {'title': 'B'}])

@app.route('/time')
def get_current_time():
	return jsonify([{'time': time.time()}])

##
# View route
##

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
  '''Return index.html for all non-api routes'''
  #pylint: disable=unused-argument
  return send_from_directory(app.static_folder, 'index.html')
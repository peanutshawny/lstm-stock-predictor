'''server/app.py - main api app declaration'''
import time
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from tensorflow import keras

from data_extract import get_yahoo_data, get_edgar_data

'''Main wrapper for app creation'''
app = Flask(__name__, static_folder='../build')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)

# load in model
model = keras.models.load_model('../models/trained_model')


##
# API routes
##


@app.route('/api/items')
def items(start, end):
    '''Sample API route for data'''

    # price data for the date entered, returns a pandas dataframe
    price_data = get_yahoo_data(start=start, end=end)

    # extract open and close from dataframe on specific date
    open_price = price_data['Open'][0]
    close_price = price_data['Close'][0]

    # Where to get fund_rate, GDP, and sentiment score?

    return jsonify([{'open': open_price}, {'close': close_price}])


@app.route('/time')
def get_current_time():
    '''Function that gets the current time, used as a date input for items function'''
    return jsonify([{'time': time.time()}])


@app.route('/api/predict')
def get_predictions(close, open, GDP, fund_rate):
    '''Model predictions'''
    diff = open - close
    x_input = [close, open, GDP, fund_rate, diff]
    return jsonify([{'output': model.predict(x_input, verbose=0)}])


@app.route('/api/wrapper')
def wrapper(start, end):
    '''Wrapper around items and get_predictions'''
    data = items(start=start, end=end)
    prediction = get_predictions(data)
    return jsonify([{'prediction': prediction}])


##
# View route
##


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    '''Return index.html for all non-api routes'''
    # pylint: disable=unused-argument
    return send_from_directory(app.static_folder, 'index.html')

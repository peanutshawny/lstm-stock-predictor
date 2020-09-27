"""server/app.py - main api app declaration"""
import time
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from tensorflow import keras

from data_extract import get_yahoo_data, get_edgar_data
from f_apiRequest import getGDP, getFund_Rate, getUnemployment

# main wrapper for app creation
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
    """Sample API route for data"""

    # price data for the date entered, returns a pandas dataframe
    price_data = get_yahoo_data(start=start, end=end)

    # extract open and close from dataframe on specific date, getting latest gdp, fund rate, and unemployment
    open_price = price_data['Open'][0]
    close_price = price_data['Close'][0]
    gdp = getGDP()
    fund_rate = getFund_Rate()
    unemployment = getUnemployment()

    return jsonify([{'open': open_price,
                     'close': close_price,
                     'gdp': gdp,
                     'fund rate': fund_rate,
                     'unemployment': unemployment}])


@app.route('/api/predict')
def get_predictions(close, open, GDP, fund_rate, unemployment):
    """Model predictions"""
    diff = open - close
    x_input = [close, open, GDP, fund_rate, unemployment, diff]
    return jsonify([{'output': model.predict(x_input, verbose=0)}])


@app.route('/api/wrapper')
def wrapper(start=time.time(), end=time.time()):
    """Wrapper around items and get_predictions, current time used as inputs"""
    data = items(start=start, end=end)
    prediction = get_predictions(data)
    return jsonify([{'prediction': prediction}])


##
# View route
##


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    """Return index.html for all non-api routes"""
    # pylint: disable=unused-argument
    return send_from_directory(app.static_folder, 'index.html')

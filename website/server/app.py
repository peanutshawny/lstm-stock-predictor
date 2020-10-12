"""server/app.py - main api app declaration"""
from datetime import date, timedelta
import numpy as np
from bs4 import BeautifulSoup
import requests
import unicodedata
import string
import re
import spacy

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from tensorflow import keras

from data_extract import get_yahoo_data, get_edgar_data, get_current_date
from data_clean import clean_text
from f_apiRequest import getGDP, getFund_Rate, getUnemployment

nlp = spacy.load('en_core_web_sm')

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
def items():
    """Sample API route for data"""

    # formatting dates to match required date inputs of each function
    yahoo_date = get_current_date('yahoo')

    edgar_date_range = get_current_date('edgar')
    edgar_start_date = edgar_date_range[0]
    edgar_end_date = edgar_date_range[1]

    # price data for the date entered, returns a pandas dataframe
    price_data = get_yahoo_data(start=yahoo_date, end=yahoo_date)

    # extract open and close from dataframe on specific date, getting latest gdp, fund rate, and unemployment
    open_price = price_data['Open'][0]
    close_price = price_data['Close'][0]
    gdp = getGDP()
    fund_rate = getFund_Rate()
    unemployment = getUnemployment()

    # 8-k links
    links = get_edgar_data(start=edgar_start_date, end=edgar_end_date)
    sentiment = clean_text(links)

    # processing to return sentiment (pos, neg, and neu)

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
def wrapper():
    """Wrapper around items and get_predictions, current time used as inputs"""
    data = items()
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


if __name__ == '__main__':
    app.run(debug=True)
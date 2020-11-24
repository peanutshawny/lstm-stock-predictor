"""server/app.py - main api app declaration"""
import boto3

import pandas as pd
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from keras.models import load_model
from numpy import array
from decimal import Decimal
import json

from src.data.data_clean import clean_text
from src.data.data_extract import get_yahoo_data, get_edgar_data, get_current_date
from src.data.f_apiRequest import getGDP, getFund_Rate, getUnemployment

# main wrapper for app creation
app = Flask(__name__, static_folder='../build')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
CORS(app)

# load in model
model = load_model('models/trained_model')

# connect to database
DB = boto3.resource('dynamodb')
table = DB.Table('stock_db')


def items():
    """function to extract all data"""

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
    diff = open_price - close_price
    gdp = getGDP()
    fund_rate = getFund_Rate()
    unemployment = getUnemployment()

    # 8-k links extracting and cleaning to get sentiment
    links = get_edgar_data(start=edgar_start_date, end=edgar_end_date)
    sentiment = links['txt_link'].map(clean_text)
    sentiment = pd.concat(sentiment.to_list())
    sentiment = pd.concat([sentiment.drop(['sentiment'], axis=1), sentiment['sentiment'].apply(pd.Series)], axis=1)

    # return average of all sentiment types
    neg = sentiment['neg'].mean()
    neu = sentiment['neu'].mean()
    pos = sentiment['pos'].mean()

    return {'date': yahoo_date,
            'close': close_price,
            'open': open_price,
            'gdp': gdp,
            'fund_rate': fund_rate,
            'neg': neg,
            'neu': neu,
            'pos': pos,
            'unemployment': unemployment,
            'diff': diff}


##
# API routes
##

@app.route('/api/db_update')
def update_db():
    """function to put data into db"""
    data = items()

    # converting dict values to decimal
    decs = {key: Decimal(str(value)) for key, value in data.items() if key != 'date'}

    # putting items into stock_db table
    table.put_item(
        Item={
            'date': data['date'],
            'close': decs['close'],
            'open': decs['open'],
            'gdp': decs['gdp'],
            'fund_rate': decs['fund_rate'],
            'neg': decs['neg'],
            'neu': decs['neu'],
            'pos': decs['pos'],
            'unemployment': decs['unemployment'],
            'diff': decs['diff']
        }
    )

    return jsonify('update successful')


@app.route('/api/predict')
def get_predictions():
    """Model predictions"""
    features = items()
    x_input = [features['close'],
               features['open'],
               features['gdp'],
               features['fund_rate'],
               features['neg'],
               features['neu'],
               features['pos'],
               features['unemployment'],
               features['diff']]

    # choose a number of time steps and features
    n_steps = 1
    n_features = 9

    x_input = array(x_input)
    x_input = x_input.reshape((1, n_steps, n_features))

    # close price prediction is in position 1
    yhat = model.predict(x_input, verbose=0)
    yhat = yhat[0][1]

    return jsonify([{'output': json.dumps(yhat.item())}])


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

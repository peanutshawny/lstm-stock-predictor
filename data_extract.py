#!/usr/bin/env python
# coding: utf-8

# In[80]:


# importing
import numpy as np
import pandas as pd

import yfinance as yf
import pandas_datareader as pdr
from TwitterAPI import TwitterAPI, TwitterPager
import csv

import datetime


# In[69]:


# getting s&p price data from yahoo finance

def get_yahoo_data():
    
    # overriding with pandas datareader
    
    yf.pdr_override()
    
    # finding s&p index ticker and getting 5 years of data
    
    sp_df = pdr.get_data_yahoo('^GSPC', start='2015-05-01', end='2020-04-30').reset_index()

    # splitting between month, day, and weekday
    
    months = []
    days = []
    weekdays = []

    for day in sp_df['Date']:
        months.append(day.month)
        days.append(day.day)
        weekdays.append(day.weekday())

    sp_df['Month'] = months
    sp_df['Day_month'] = days
    sp_df['Day_week'] = weekdays
    
    return(sp_df)


# In[70]:


# twitter API authentication

def get_twitter_authentication():
    
    # variables that contain user credentials to access twitter api
    
    ACCESS_TOKEN = '1255891281752010754-VrK3kU7JvarLjVMsJets7QTkinwuZx'
    ACCESS_SECRET = 'dVeuWeSpdFe91lngima25xQhlP5ijiDC2iYiP0mNKU2cC'
    CONSUMER_KEY = 'UUCzKktOILbxhagMxyyCyjF7E'
    CONSUMER_SECRET = 'LXYmgtey0ZoB4oayVEWvgjZ0XUxmwSVuR2bNW9fXWVvZC5klVs'

    api = TwitterAPI(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    
    return(api)


# In[81]:


# getting tweets

def get_tweets():
    
    client = get_twitter_authentication()

    # connecting to fullarchive endpoint and dev env

    PRODUCT = 'fullarchive'
    LABEL = 'prod'
    
    csv_file = open('D:/Python/stock predictor/tweet.csv', 'w')
    csv_writer = csv.writer(csv_file)

    # iterate through all pages and appending username, tweet, and date

    pager = TwitterPager(client, 'tweets/search/%s/:%s' % (PRODUCT, LABEL), 
                       {'query':'#stocks OR #markets OR #S&P500',
                       'fromDate': '201505010000',
                       'toDate': '202004300000',
                       'maxResults': 80}
                      )

    for item in pager.get_iterator():
        if pager.status_code != 200:
            break
        
        # writing to csv row by row 
        
        csv_writer.writerow([item['created_at'], 
                            item['user']['screen_name'], 
                            item['text'] if 'text' in item else item])
    
    return


#!/usr/bin/env python
# coding: utf-8

# importing
import numpy as np
import pandas as pd

import yfinance as yf
import pandas_datareader as pdr
import csv
import datetime

import requests
from bs4 import BeautifulSoup
from time import sleep


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

    return sp_df


def get_edgar_data():
    # getting CIK for every company in the s&p 500 from wikipedia

    wiki_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    cik_df = pd.read_html(wiki_url, header=0, index_col=0)[0]
    cik_list = list(cik_df['CIK'])

    # creating empty dataframe to append all other dataframes with 8-k links
    doc_df = pd.DataFrame()

    for cik in cik_list:

        try:

            # defining endpoint and parameters for every company in the s&p
            url = 'https://www.sec.gov/cgi-bin/browse-edgar'
            params = {'action': 'getcompany',
                      'CIK': cik,
                      'type': '8-K',
                      'output': 'xml',
                      'dateb': '20200430',
                      'datea': '20150501',
                      'start': '',
                      'count': '100'}

            # getting response from EDGAR database
            sec_response = requests.get(url=url, params=params)

            # creating soup to parse xml
            soup = BeautifulSoup(sec_response.content, 'xml')

            # getting link to 8-k document
            urls = soup.findAll('filingHREF')
            html_list = []

            # html version of links
            for url in urls:
                url = url.string

                if url.split('.')[len(url.split('.')) - 1] == 'htm':
                    txt_link = url + 'l'
                    html_list.append(txt_link)

            html_list = pd.Series(html_list).astype(str)

            # list of links
            doc_list = html_list.str.replace('-index.html', '.txt').values.tolist()

            # creating dataframe to append the link of each company

            df = pd.DataFrame({'cik': [cik] * len(doc_list),
                               'txt_link': doc_list})

            doc_df = doc_df.append(df)

        except requests.exceptions.ConnectionError:
            sleep(.1)

    return doc_df

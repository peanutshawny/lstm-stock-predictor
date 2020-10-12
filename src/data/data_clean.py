#!/usr/bin/env python
# coding: utf-8

# importing
import numpy as np
from bs4 import BeautifulSoup
import requests
import unicodedata
import string
import re
import spacy

nlp = spacy.load('en_core_web_sm')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords


# cleaning the price data

def clean_close(sp_df):
    # adding normalized percentage changes

    sp_df['range'] = sp_df['High'] - sp_df['Low']
    sp_df['close_norm'] = sp_df['Close'].pct_change()
    sp_df['low_norm'] = sp_df['Low'].pct_change()
    sp_df['high_norm'] = sp_df['High'].pct_change()
    sp_df['open_norm'] = sp_df['Open'].pct_change()
    sp_df['vol_norm'] = sp_df['Volume'].pct_change()
    sp_df['range_norm'] = sp_df['range'].pct.change()

    # dropping unnecessary features

    sp_df.drop(columns=['Date', 'Stock Splits', 'Dividends', 'Close',
                        'Open', 'Low', 'High', 'Volume', 'range'], inplace=True)

    return sp_df


# parsing text from 8-ks

def get_soup(link):
    '''
    function that returns soup object of a 8-k link
    '''
    try:
        request = requests.get(link)
        soup = BeautifulSoup(request.content, 'html5lib', from_encoding='ascii')

    except:
        soup = 'na'

    return soup


def get_date(soup):
    '''
    function that returns date of a soup object
    '''
    try:
        date = soup.find('acceptance-datetime').string[:8]

        # change date formatting to YYYY-MM-DD
        date = date[:4] + '-' + date[4:6] + '-' + date[6:]

    # setting date as 00000000 if no date is found
    except AttributeError:
        date = '0000-00-00'

    return date


# empty numpy arrays for dates, finished docs (eventually sentiment)
date_list = sentiment_list = np.empty(shape=0, dtype=object)

# cleaning text by removing punctuation and stopwords, as well as lemmatization
punctuations = string.punctuation
sw = stopwords.words('english')


def clean_text(link, date_list=date_list, sentiment_list=sentiment_list):
    '''
    function that utilizes get_soup and get_date to process text, outputs sentiment scores and dates
    '''

    # requesting the doc from link
    soup = get_soup(link)

    # getting date from soup
    date = get_date(soup)
    date_list = np.append(date_list, [date])

    # extracting text from soup
    try:
        for section in soup.findAll('html'):

            try:
                # removing tables
                for table in section('table'):
                    table.decompose()

                # converting to unicode
                section = unicodedata.normalize('NFKD', section.text)
                section = section.replace('\t', ' ').replace('\n', '').replace('/s', '').replace('\'', '')

            except AttributeError:
                section = str(section.encode('utf-8'))

            # joining, removing unecessary characters, and truncating text
            text = ''.join((section))
            text = re.sub('\s+', ' ', text).strip()
            text = text[:40000]

            # creating spacy nlp variable to tokenize and remove punctuation
            doc = nlp(text)

            doc = [token.lemma_.lower().strip() for token in doc]
            doc = [token for token in doc if token.isalpha()]
            doc = [token for token in doc if token not in punctuations and token not in sw]

            # joining text and getting sentiment
            doc = ' '.join(doc)

            analyzer = SentimentIntensityAnalyzer()
            sentiment = analyzer.polarity_scores(doc)

            sentiment_list = np.append(sentiment_list, sentiment)

    # output blank tokens and 0 sentiment for any link in case of error

    except:
        sentiment = np.ndarray({'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0})
        sentiment_list = np.append(sentiment_list, sentiment)

    documents = [date_list, sentiment_list]

    return documents

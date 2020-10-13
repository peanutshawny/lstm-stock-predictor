#!/usr/bin/env python
# coding: utf-8

# importing
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import unicodedata
import string
import re
import spacy

nlp = spacy.load('en_core_web_sm')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords


# parsing text from 8-ks

def get_soup(link):
    """
    function that returns soup object of a 8-k link
    """
    try:
        request = requests.get(link)
        soup = BeautifulSoup(request.content, 'html5lib', from_encoding='ascii')

    except:
        soup = 'na'

    return soup


# empty numpy arrays for sentiment
sentiment_list = np.empty(shape=0, dtype=object)

# cleaning text by removing punctuation and stopwords, as well as lemmatization
punctuations = string.punctuation
sw = stopwords.words('english')


def clean_text(link, sentiment_list=sentiment_list):
    """
    function that generates a soup to process text and output sentiment scores
    """

    # requesting the doc from link
    soup = get_soup(link)

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
            text = ''.join(section)
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

    # output blank tokens and 0 sentiment for any link in case of error

    except:

        # outputs empty sentiment when no sentiment it present
        sentiment = np.ndarray({'neg': 0, 'neu': 0, 'pos': 0, 'compound': 0})

    sentiment_list = np.append(sentiment_list, sentiment)

    # transposing each type of sentiment (pos, neg, neu) into separate features
    sentiment_df = pd.DataFrame({'sentiment': sentiment_list})
    sentiment_df = sentiment_df['sentiment'].apply(pd.Series)

    # return average of all sentiment types
    pos = sentiment_df['pos'].mean()
    neg = sentiment_df['neg'].mean()
    neu = sentiment_df['neu'].mean()

    return {'pos': pos, 'neg': neg, 'neu': neu}

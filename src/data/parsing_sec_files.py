#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import unicodedata
import datetime

import string
import re
import spacy
nlp = spacy.load('en_core_web_sm')

import nltk
nltk.download('stopwords')

from nltk.corpus import stopwords

cik_df = pd.read_csv('8-k_links.csv')

# empty numpy arrays for dates, text, and finished docs
date_list = doc_list = np.empty(shape=len(cik_df['txt_link']), dtype=object)

# cleaning text by removing punctuation and stopwords, as well as lemmatization
punctuations = string.punctuation
stopwords = stopwords.words('english')

def clean_text(link, date_list=date_list, doc_list=doc_list):
    '''
    function that returns soup object of 8-k text link
    '''

    # requesting the doc from link
    try:
        request = requests.get(link)
        soup = BeautifulSoup(request.content, 'html5lib', from_encoding = 'ascii')

    except:
        soup = 'na'

    # getting date from soup
    try:
        date = soup.find('acceptance-datetime').string[:8]

    # setting date as 00000000 if no date is found
    except AttributeError:
        date = '00000000'

    date_list = np.append(date_list, date)

    # extracting text from soup
    try:
        for section in soup.findAll('html'): 

            try:
                # removing tables
                for table in section('table'):
                    table.decompose()

                # converting to unicode
                section = unicodedata.normalize('NFKD', section.text)
                section = section.replace('\t', ' ').replace('\n', '').replace('/s', '').replace('\'','')

            except AttributeError:
                section = str(section.encode('utf-8'))
        
            # joining, removing unecessary characters, and truncating text 
            text = ''.join((section))
            text = re.sub( '\s+', ' ', text).strip()
            text = text[:40000]

            # creating spacy nlp variable to tokenize and remove punctuation
            doc = nlp(text, disable=['parser', 'ner'])

            doc = [token.lemma_.lower().strip() for token in doc]
            doc = [token for token in doc if token.isalpha()]
            doc = [token for token in doc if token not in punctuations and token not in stopwords]

            doc_list = np.append(doc, doc_list)

    # output blank tokens for any link in case of error

    except:
        doc = []
        doc_list = np.concatenate((doc, doc_list))

    print(doc)

    return [date_list, doc_list]

# mapping results to links
result  = cik_df['txt_link'].map(clean_text)

dates = result[0]
docs = result[1]

if len(dates) == len(cik_df['txt_link']):
    cik_df['date'], cik_df['processed_tokens'] = dates, docs

else:
    cik_df = pd.DataFrame({'date': dates, 'tokens': docs})

cik_df.to_csv('processed_tokens.csv', index=False)
# def get_soup(link):
#     '''
#     simple function that returns soup object of 8-k text link
#     '''

#     # requesting the doc from link
    
#     request = requests.get(link)

#     try:
#         soup = BeautifulSoup(request.content, 'html.parser', from_encoding = 'ascii')

#     except:
#         soup = 'na'

#     return soup


# def find_date(soup, date_list=date_list):
#     '''
#     function to find the date from the soup of 8-k links
#     '''
#     # getting dates
#     try:
#         date = soup.find('acceptance-datetime').string[:8]

#     except AttributeError:
#         date = '00000000'

#     date = datetime.datetime.strptime(date,'%Y%m%d')

#     date_list = np.append(date_list, date)
    
#     return date_list


# def clean_text(soup, doc_list=doc_list):
#     '''
#     function that performs tokenization, lemmatization, and removes stopwords from text
#     '''

#     try:
#     # extracting text from soup
#         for section in soup.findAll('html'): 
#             try:

#                 # removing tables
#                 for table in section('table'):
#                     table.decompose()

#                 # converting to unicode
#                 section = unicodedata.normalize('NFKD', section.text)
#                 section = section.replace('\t', ' ').replace('\n', '').replace('/s', '').replace('\'','')

#             except AttributeError:
#                 section = str(section.encode('utf-8'))
        
#             # joining, removing unecessary characters, and truncating text 
#             text = ' '.join((section))
#             text = re.sub( '\s+', ' ', text).strip()
#             text = text[:35000]

#             # creating spacy nlp variable
#             doc = nlp(text, disable=['parser', 'ner'])

#             doc = [token.lemma_.lower().strip() for token in doc]
#             doc = [token for token in doc if token.isalpha()]
#             doc = [token for token in doc if token not in punctuations and token not in stopwords]

#             doc_list = np.append(doc, doc_list)

#     except:
#         doc = []
#         doc_list = np.append(doc, doc_list)

#     return doc_list


# cik_df['soup'] = cik_df['txt_link'].map(get_soup)

# cik_df.to_csv('processed_soup.csv', index=False)
# cik_df = pd.read_csv('processed_soup.csv')

# cik_df['date'] = cik_df['soup'].map(find_date)

# cik_df.to_csv('processed_soup_date.csv', index=False)
# cik_df = pd.read_csv('processed_soup_date.csv')

# cik_df['processed_tokens'] = cik_df['soup'].map(clean_text)
# cik_df.drop(columns='soup')

# cik_df.to_csv('processed_tokens.csv', index=False)



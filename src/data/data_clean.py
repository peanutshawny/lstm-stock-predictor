#!/usr/bin/env python
# coding: utf-8

# importing
import numpy as np
import pandas as pd

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
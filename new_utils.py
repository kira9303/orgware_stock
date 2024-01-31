import pandas as pd
import numpy as np
import yfinance as yf
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import json


def is_Suppport_Level(df, i):
  support = df['Low'][i] < df['Low'][i - 1] and df['Low'][i] < df['Low'][i + 1] and df['Low'][i + 1] < df['Low'][i + 2] and df['Low'][i - 1] < df['Low'][i - 2]
  return support


def is_Resistance_Level(df, i):
  resistance = df['High'][i] > df['High'][i - 1] and df['High'][i] > df['High'][i + 1] and df['High'][i + 1] > df['High'][i + 2] and df['High'][i - 1] > df['High'][i - 2]
  return resistance



def get_preds(data):
    df = yf.download(tickers=data, period='2d', interval='1h')

    df['Date'] = pd.to_datetime(df.index)

    df['Date'] = df['Date'].apply(mpl_dates.date2num)

    df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

    levels = []
    level_types = []

    for i in range(2, df.shape[0] - 2):

        if is_Suppport_Level(df, i):
            levels.append((i, df['Low'][i].round(2), df['Close'][i].round(2)))
            level_types.append('Support')
            # df.at[i, 'detections'] = 1
            # df['supps'] = 1
            # df['resistance'] = 0

        if is_Resistance_Level(df, i):
            levels.append((i, df['High'][i].round(2), df['Close'][i].round(2)))
            level_types.append('Resistance')
            # df.at[i, 'detections'] = 2
            # df['supps'] = 0


    # levels and levels_type
    print("printing the lenght of found res and supps")
    print(len(levels))
    print(len(level_types))

    indices_supp = []
    indices_res = []

    for i in range(0, len(level_types)):
        if (level_types[i] == 'Support'):
            indices_supp.append(levels[i][0])
        if (level_types[i] == 'Resistance'):
            indices_res.append(levels[i][0])


    zero_list = [0] * len(df['Close'])

    for val in indices_supp:
        zero_list[val] = 1

    for new_val in indices_res:
        zero_list[new_val] = 2

    df['new_detections'] = zero_list

    #print(zero_list)

    tail = df.tail(12)

    new_tail = tail['new_detections'].tolist()

    curr = 0
    for new in range(0, len(new_tail)):
        if(new_tail[new]==2 or new_tail[new]==1):
            curr = new_tail[new]

    return curr










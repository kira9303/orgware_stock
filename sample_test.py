import pandas as pd
import numpy as np
import yfinance as yf
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = [12, 7]
plt.rc('font', size=14)

ticker_symbol = '4063.T'
ticker = yf.Ticker(ticker_symbol)


df = yf.download(tickers=ticker_symbol, period='30d', interval='1h')


start_date = '2023-12-1'
end_date = '2024-1-31'

#df = ticker.history(interval='1h', start=start_date, end=end_date)

df['Date'] = pd.to_datetime(df.index)


df['Date'] = df['Date'].apply(mpl_dates.date2num)



df = df.loc[:,['Date', 'Open', 'High', 'Low', 'Close']]



def is_Suppport_Level(df, i):
  support = df['Low'][i] < df['Low'][i - 1] and df['Low'][i] < df['Low'][i + 1] and df['Low'][i + 1] < df['Low'][i + 2] and df['Low'][i - 1] < df['Low'][i - 2]
  return support


def is_Resistance_Level(df, i):
  resistance = df['High'][i] > df['High'][i - 1] and df['High'][i] > df['High'][i + 1] and df['High'][i + 1] > df['High'][i + 2] and df['High'][i - 1] > df['High'][i - 2]
  return resistance

# Creating a list and feeding it the identified support and resistance levels via the Support and Resistance functions
levels = []
level_types = []


for i in range(2, df.shape[0] - 2):

  if is_Suppport_Level(df, i):
    levels.append((i, df['Low'][i].round(2), df['Close'][i].round(2)))
    level_types.append('Support')
    #df.at[i, 'detections'] = 1
    #df['supps'] = 1
    #df['resistance'] = 0


  if is_Resistance_Level(df, i):
    levels.append((i, df['High'][i].round(2), df['Close'][i].round(2)))
    level_types.append('Resistance')
    #df.at[i, 'detections'] = 2
    #df['supps'] = 0



supp_count = 0
res_count = 0
#levels and levels_type
print("printing the lenght of found res and supps")
print(len(levels))
print(len(level_types))

indices_supp = []
indices_res = []



for i in range(0, len(level_types)):
  if(level_types[i]=='Support'):
    indices_supp.append(levels[i][0])
  if(level_types[i]=='Resistance'):
    indices_res.append(levels[i][0])

print(indices_res)
print(indices_supp)

print(levels)
print(level_types)

zero_list = [0] * len(df['Close'])

for val in indices_supp:
  zero_list[val] = 1

for new_val in indices_res:
  zero_list[new_val] = 2

print(zero_list)

df['new_detections'] = zero_list

#print(df.tail(12))

print(df.tail(12))

tail = df.tail(12)

new_tail = tail['new_detections'].tolist()
print(new_tail)

curr = 0
for new in range(0, len(new_tail)):
  if(new_tail[new] == 2 or new_tail[new] == 1):
    curr = new_tail[new]


print("new curr is here")
print(curr)
#print(df)

#print(levels)

# Plotting the data
fig, ax = plt.subplots()
candlestick_ohlc(ax, df.values, width=0.3, colorup='green', colordown='red', alpha=0.5)
date_format = mpl_dates.DateFormatter('%d %b %Y')
ax.xaxis.set_major_formatter(date_format)
fig.autofmt_xdate()
fig.tight_layout()


for level, level_type in zip(levels, level_types):
  plt.hlines(level[1],
             xmin=df['Date'][level[0]],
             xmax=max(df['Date']),
             colors='blue')
  plt.text(df['Date'][level[0]], level[1], (str(level_type) + ': ' + str(level[1]) + ' '), ha='right', va='center',
           fontweight='bold', fontsize='x-small')
  plt.title('Support and Resistance levels for ' + ticker_symbol, fontsize=24, fontweight='bold')

  plt.savefig("sine_wave.png")
  fig.show()

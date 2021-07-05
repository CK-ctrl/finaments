# This where I try and test different code scripts related to finaments.
import time
import numpy as np
import pandas as pd
import requests as rq
import mplfinance as mpf
import matplotlib.pyplot as plt

from pprint import pprint
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries

API_KEY = '2V99TLARJ7RZ5L2N'		 # This is my alpha vantage key, generate your own key.

QUOTE = ['GLOBAL_QUOTE','SYMBOL_SEARCH']

TS = ['TIME_SERIES_INTRADAY',				#0
		'TIME_SERIES_INTRADAY_EXTENDED',	#1
		'TIME_SERIES_DAILY',				#2
		'TIME_SERIES_DAILY_ADJUSTED',		#3
		'TIME_SERIES_WEEKLY',				#4
		'TIME_SERIES_WEEKLY_ADJUSTED',		#5
		'TIME_SERIES_MONTHLY',				#6
		'TIME_SERIES_MONTHLY_ADJUSTED']		#7

FN = ['OVERVIEW',				#0
		'EARNINGS',				#1
		'INCOME_STATEMENT',		#2
		'BALANCE_SHEET',		#3
		'CASH_FLOW',			#4
		'LISTING_STATUS',		#5
		'EARNINGS_CALENDAR',	#6
		'IPO_CALENDAR']			#7

URL = 'https://www.alphavantage.co/query'
TOKEN = 'AAPL'

# This fuction returns pandas dataframe.
def get_tsdata(tick, type, interval=None, Slice=None):
	payload = {'apikey':API_KEY, 'function':TS[type], 'symbol':tick}
	if interval is not None:
		payload['interval'] = interval
		if Slice is not None:
			payload['slice'] = Slice

	r = rq.get(URL, params=payload)
	data = r.json()
	keys = list(data.keys())

	df = pd.DataFrame(data[keys[1]]).T
	if type in [3,5,7]:
		df.columns = ['open','high','low','close','adjusted close','volume','dividend amount','split coefficient']
	else:
		df.columns = ['open','high','low','close','volume']
	return len(df.columns)

# This fuction returns pandas dataframe.
def get_tsdata_csv(tick, type, interval=None, Slice=None):
	payload = {'apikey':API_KEY, 'function':TS[type], 'symbol':tick, 'datatype':'csv'}
	if interval is not None:
		payload['interval'] = interval
		if Slice is not None:
			payload['slice'] = Slice

	r = rq.get(URL,params=payload)
	return pd.read_csv(r.url, index_col=0)

# This function returns python dictionary, will all overview information about give company.
def get_overview(tick):
	payload = {'apikey':API_KEY, 'function':FN[0], 'symbol':tick}
	r = rq.get(URL, params=payload)
	data = r.json()
	return data

# This function returns pandas dataframe tuple consisting of annual and quaterly dataframes.
def get_fndata(tick,type):
	payload = {'apikey':API_KEY, 'function':FN[type], 'symbol':tick}
	r = rq.get(URL, params=payload)
	data = r.json()
	keys = list(data.keys())

	annual = pd.DataFrame(data[keys[1]])
	quaterly = pd.DataFrame(data[keys[2]])
	annual.set_index('fiscalDateEnding',inplace=True)
	quaterly.set_index('fiscalDateEnding',inplace=True)
	return (annual,quaterly)

# annual_report, quaterly_report = get_fndata(TOKEN,1)
# annual_report, quaterly_report = get_fndata(TOKEN,2)
# annual_report, quaterly_report = get_fndata(TOKEN,3)
# annual_report, quaterly_report = get_fndata(TOKEN,4)

data = get_tsdata_csv(TOKEN,2)
daily = data.drop('volume', axis=1)

index = pd.Series(daily.index)
newindex = list()

for i in index:
	newindex.append(datetime.strptime(i,'%Y-%m-%d'))

daily.index = newindex
mpf.plot(daily, type='candle')
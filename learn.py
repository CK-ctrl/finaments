# This where I try and test different code scripts related to finaments.

import numpy as np
import pandas as pd
import requests as rq
import mplfinance as mpf
import matplotlib.pyplot as plt

from pprint import pprint
from datetime import datetime


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
TOKEN = 'TSLA'

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
	# print(r.url)
	data = pd.read_csv(r.url, parse_dates=['timestamp'],index_col=0)
	data = data.reindex(index=data.index[::-1])
	return data

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
	return annual,quaterly


def gett():
	return get_overview(TOKEN)

# annual_report, quaterly_report = get_fndata(TOKEN,1)
# annual_report, quaterly_report = get_fndata(TOKEN,2)
# annual_report, quaterly_report = get_fndata(TOKEN,3)
# annual_report, quaterly_report = get_fndata(TOKEN,4)


# mpf.plot(data, type='candle', mav=(5,10,20), volume=True)


def test():
	temp = gett()
	print(temp['52WeekHigh'])

if __name__ == "__main__":
	test()
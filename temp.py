import pandas as pd
import requests as rq
from pprint import pprint

API_KEY = '2V99TLARJ7RZ5L2N'
URL = 'https://www.alphavantage.co/query'

action = True
while action:
	token = input('Enter stock Token: ')
	payload = {'apikey':API_KEY, 'function':'OVERVIEW', 'symbol':token}
	r = rq.get(URL, params=payload)
	print(r.status_code)
	data = r.json()
	pprint(data)
	action = input('Do you want to continue(True/False)')

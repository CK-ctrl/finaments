# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, BooleanField
# from wtforms.validators import DataRequired, Length, Email, EqualTo

# class RegistrationForm(FlaskForm):
# 	# This will later be used as label in our forms
# 	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
# 	email = StringField('Email', validators=[DataRequired(), Email()])
# 	password = PasswordField('Password', validators=[DataRequired(), EqualTo()])
# 	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
# 	submit = SubmitField('Sign Up')

# class LoginForm(FlaskForm):
# 	# This will later be used as label in our forms
# 	email = StringField('Email', validators=[DataRequired(), Email()])
# 	password = PasswordField('Password', validators=[DataRequired(), EqualTo()])
# 	remember = BooleanField('Remember Me')
# 	submit = SubmitField('Login')

import pandas as pd
import requests as rq

API_KEY = '2V99TLARJ7RZ5L2N'
URL = 'https://www.alphavantage.co/query'

payload = {'apikey':API_KEY, 'function':'LISTING_STATUS'}

r = rq.get(URL, params=payload)
print(r.status_code)

data = pd.read_csv(r.url, index_col=0)
data = data[data['assetType'] == 'Stock']
data.drop(columns=['assetType', 'ipoDate', 'delistingDate', 'status'], inplace=True)
print(data.shape)
data.dropna(inplace=True)
print(data.shape)
data = data[data['exchange'] != 'NYSE ARCA']
print(data.shape)
print(data)
tickers = data.index.tolist()
print(len(tickers),tickers)

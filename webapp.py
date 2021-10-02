from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import mplfinance as mpf
import pandas as pd
import learn
import io 

app = Flask(__name__)
app.config['SECRET_KEY'] = '627f7d4c934190ad0d323c386ccdc8d6'

class SearchForm(FlaskForm): 		# This is one of the main funcitons.
	token = StringField('Token')
	search = SubmitField('Search')

@app.route('/<token>')
def index(token):
	data = learn.gett(token)
	overview = data[0]
	earnings_a, earnings_q = data[1]
	income_a, income_q = data[2]
	balance_a, balance_q = data[3]
	cashflow_a, cashflow_q = data[4]
	return render_template('index.html', title=token, data=overview, 
				tables=[earnings_q.to_html(classes='data', header=True), #titles='earnings_q.columns.values'), 
						earnings_a.to_html(classes='data', header=True), #titles='earnings_a.columns.values'),
						income_q.to_html(classes='data', header=True), #titles='income_q.columns.values'), 
						income_a.to_html(classes='data', header=True), #titles='income_a.columns.values'),
						balance_q.to_html(classes='data', header=True), #titles='balance_q.columns.values'), 
						balance_a.to_html(classes='data', header=True), #titles='balance_a.columns.values'),
						cashflow_q.to_html(classes='data', header=True), #titles='cashflow_q.columns.values'), 
						cashflow_a.to_html(classes='data', header=True)]) #titles='cashflow_a.columns.values')])

@app.route('/', methods=['GET','POST'])
def search():														# This is the search function, styling and auto complete feature remaining.
	form = SearchForm()
	if (form.validate_on_submit()):
		return redirect(url_for('index', token=form.token.data))
	return render_template('search.html', form=form, tickers=learn.tickers)

@app.route('/chart/<token>')										# This is a differnt version with price action some trading sessions.
def chart(token):
	data = learn.gets(token)
	overview = data[0]
	ts = data[1]
	mpf.plot(ts,type="candle", volume=True, savefig='static/plots/plot.png')
	return render_template('chart.html', data=overview)

@app.route('/test/<token>')
def test(token):
	return learn.get_overview(token)

@app.route('/ttest/<token>')
def ttest(token):
	data = learn.get_tsdata_csv(token,2)
	return render_template('ttest.html', data=data)

if __name__ == "__main__":
	app.run(debug=True)
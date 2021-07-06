from flask import Flask, render_template, url_for
import learn

app = Flask(__name__)

app.config['SECRET_KEY'] = '627f7d4c934190ad0d323c386ccdc8d6'

@app.route('/')
def index():
	data = learn.gett()
	overview = data[0]
	earnings_a, earnings_q = data[1]
	income_a, income_q = data[2]
	balance_a, balance_q = data[3]
	cashflow_a, cashflow_q = data[4]
	return render_template('index.html', data=overview, earnings=earnings_a, income=income_a, balance=balance_a, cashflow=cashflow_a)

if __name__ == "__main__":
	app.run(debug=True)
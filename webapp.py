from flask import Flask, render_template, url_for
import learn

app = Flask(__name__)
@app.route('/')
def hello():
	return render_template('index.html',data=learn.gett())

if __name__ == "__main__":
	app.run(debug=True)
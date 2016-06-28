import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(
	os.environ['DB_PORT_27017_TCP_ADDR'], 
	27017)
db = client.printdb


@app.route('/')
def queue():

	return render_template('index.html')

@app.route('/view')
def view():

	_items = db.printdb.find()
	items = [item for item in _items]

	return render_template('queue.html', items=items)

@app.route('/submit')
def submit():

	return render_template('submit.html')

@app.route('/new', methods=['POST'])
def new():

	item = {
		'name': request.form['inputName'],
		'company': request.form['inputCompany'],
		'title': request.form['inputTitle'],
		'email': request.form['inputEmail'],
		'printer': request.form['select'],
		'additional': request.form['inputAdditional']
	}

	db.printdb.insert_one(item)

	return redirect(url_for('queue'))


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
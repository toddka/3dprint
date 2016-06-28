import os
from flask import Flask, redirect, url_for, request, render_template
from pymongo import MongoClient
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['.stlt', '.rar', '.mp3'])

app = Flask(__name__)
app.debug = True

client = MongoClient('mongodb://localhost:27017/')
# client = MongoClient(
# 	os.environ['DB_PORT_27017_TCP_ADDR'], 
# 	27017)

db = client.printdb

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

	f = request.files['file']
	print f.filename
	# if f and allowed_file(f.filename):
	if f:
		f.save('files/' + request.form['inputCompany'] + "_" + secure_filename(f.filename))

	item = {
		'name': request.form['inputName'],
		'company': request.form['inputCompany'],
		'title': request.form['inputTitle'],
		'email': request.form['inputEmail'],
		'printer': request.form['select'],
		'additional': request.form['inputAdditional'],
	}

	db.printdb.insert_one(item)

	return redirect(url_for('view'))


if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)
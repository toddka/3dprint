import os
import smtplib
from flask import Flask, redirect, url_for, request, render_template, make_response
from flask_mail import Mail, Message
from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = set(['.stlt', '.rar', '.mp3'])

app = Flask(__name__)
app.config.update(
	DEBUG=True
	)


connection = MongoClient('ds025583.mlab.com', 25583)
db = connection['printdb']
db.authenticate('admin', 'Impact!Now')
fs = gridfs.GridFS(db)


# db = client.printdb

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

@app.route('/admin')
def admin():

	_items = db.printdb.find()
	items = [item for item in _items]

	return render_template('admin.html', items=items)

@app.route('/success')
def success():

	return render_template('success.html')

@app.route('/new', methods=['POST'])
def new():

	f = request.files['file']
	print f.filename
	# if f and allowed_file(f.filename):
	if f:
	    b = fs.put(f, filename=request.form['inputCompany'] + "_" + secure_filename(f.filename))
# 		f.save('files/' + request.form['inputCompany'] + "_" + secure_filename(f.filename))

	item = {
		'name': request.form['inputName'],
		'company': request.form['inputCompany'],
		'title': request.form['inputTitle'],
		'email': request.form['inputEmail'],
		'printer': request.form['select'],
		'additional': request.form['inputAdditional'],
		'_id': b #storing file's id to retrieve from gridFS later
	}

	db.printdb.insert_one(item)

	to = 'tashley@masschallenge.org'
	gmail_user = 'tashley@masschallenge.org'
	gmail_pwd = OMMITTED
	smtpserver = smtplib.SMTP("smtp.gmail.com",587)
	smtpserver.ehlo()
	smtpserver.starttls()
	smtpserver.ehlo
	smtpserver.login(gmail_user, gmail_pwd)
	header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:MADE@: A new print job has been added to the queue. \n'
	msg = header + request.form['inputCompany'] + ' has created a new print job titled ' + request.form['inputTitle'] +' for the '+ request.form['select'] + ' printer.'
	smtpserver.sendmail(gmail_user, to, msg)
	smtpserver.close()
	print "done"

	return redirect(url_for('view'))

@app.route('/get-file/<_id>')
def get_file(_id=None):

    if _id is not None:
        f = fs.find_one({'_id': ObjectId(_id)})
        job = db.printdb.find_one({'_id': ObjectId(_id)})
        name = job['company'] + "_" + job['title'] 

        response = make_response(f.read())
    	response.headers['Content-Type'] = 'application/octet-stream'
    	response.headers["Content-Disposition"] = "attachment; filename={}".format(name)
    	return response

    return render_template('download.html', names=fs.list())

@app.route('/delete-file/<_id>')
def delete_file(_id=None, methods=['GET']):

    if _id is not None:
    	print _id
        fs.delete(ObjectId(_id))
        job = db.printdb.delete_one({'_id': ObjectId(_id)})

    return redirect(url_for('admin'))

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)

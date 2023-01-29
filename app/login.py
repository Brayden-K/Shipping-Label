from flask import render_template, jsonify, abort, request, redirect, session, flash, url_for
from app import app
import requests, datetime
from pprint import pprint

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return redirect(url_for('index'))

	if session.get('loggedin'):
			flash('You are already logged in.')
			return redirect(url_for('index'))

	if not 'username' in request.form:
		flash('Username is required')
		return redirect(url_for('index'))

	if not 'password' in request.form:
		flash('Please enter your password')
		return redirect(url_for('index'))

	username = request.form.get('username')
	password = request.form.get('password')
	user = app.db.GetLogin(username, password)
	if not user:
		flash('Invalid username or password')
		return redirect(url_for('index'))

	session['loggedin'] = True
	session['username'] = user['email']
	flash('You have successfully logged in')
	return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		return redirect(url_for('index'))

	if session.get('loggedin'):
			flash('You are already logged in.')
			return redirect(url_for('index'))

	if not 'email' in request.form:
		flash('Email is required')
		return redirect(url_for('index'))
	
	if not 'password' in request.form:
		flash('Please enter your password')
		return redirect(url_for('index'))
	
	if not 'confirmPassword' in request.form:
		flash('Please confirm your password')
		return redirect(url_for('index'))

	settings = app.db.GetSettings()
	if settings['requireCaptcha']:
		if not 'g-recaptcha-response' in request.form:
			flash('Please complete the captcha')
			return redirect(url_for('index'))
		if not checkCaptcha(request.form.get('g-recaptcha-response')):
			flash('Invalid captcha')
			return redirect(url_for('index'))

	email = request.form.get('email')
	password = request.form.get('password')
	confirmPassword = request.form.get('confirmPassword')

	if not password == confirmPassword:
		flash('Your passwords do not match.')
		return redirect(url_for('index'))

	# Submit
	data = {
		'email': email,
		'password': password
	}

	try:
		app.db.Insert('users', data)
	except:
		flash('Something went wrong with registration.')
		return redirect(url_for('index'))
	user = app.db.GetLogin(email, password)
	session['loggedin'] = True
	session['username'] = user['email']
	flash('Successfully registered and signed in.')
	return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    flash('You have successfully logged out')
    return redirect(url_for('index'))

def checkCaptcha(resp):
	settings = app.db.GetSettings()
	data = {
		'secret': settings['captchaSecret'],
		'response': resp
	}
	r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
	if r.json()['success']:
		return True
	else:
		return False
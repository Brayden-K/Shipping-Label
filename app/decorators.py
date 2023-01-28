from flask import render_template, redirect, url_for, session, flash, abort
from app import app
from functools import wraps

def login_required(f):
	"""
	Sets @login_required decorator to require
	login on authenticated pages
	"""
	@wraps(f)
	def wrap(*args, **kwargs):
		# if user is not logged in, redirect to login page      
		if not session.get('loggedin'):
			flash('You need to be logged in to view this page.')
			return redirect(url_for('index'))
		return f(*args, **kwargs)
	return wrap

def admin_required(f):
	"""
	Sets @admin_required decorator to require
	admin on admin pages
	"""
	@wraps(f)
	def wrap(*args, **kwargs):
		# if user is not logged in, redirect to login page      
		if not session:
			return redirect(url_for('login'))

		user = app.db.GetUserByUsername(session['username'])
		if not user['admin']:
			return redirect(abort(404))
		return f(*args, **kwargs)
	return wrap
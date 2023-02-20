from flask import render_template, jsonify, request, redirect, session, flash, url_for, send_from_directory, abort
from app import app
from app.decorators import login_required
from app.errors import page_not_found, webhook
import time, os
from pprint import pprint

@app.route('/order')
@login_required
def order():
	templates = app.db.GetTemplates(app.db.GetUserByEmail(session['username'])['id'])
	providers = app.db.GetProviders()
	return render_template('order.html', templates=templates, providers=providers)

@app.route('/templates', methods=['GET', 'POST'])
@login_required
def templates():
	if request.method == 'GET':
		templates = app.db.GetTemplates(app.db.GetUserByEmail(session['username'])['id'])
		return render_template('templates.html', templates=templates)

	if not request.form.get('action'):
		flash('Something went wrong.')
		return redirect(url_for('templates'))

	match request.form.get('action'):
		case 'addTemplate':
			data = request.form.to_dict()
			del data['action']
			data['ownerId'] = app.db.GetUserByEmail(session['username'])['id']
			app.db.Insert('templates', data)
			flash('Template added.')
			return redirect(url_for('templates'))

		case 'editTemplate':
			data = request.form.to_dict()
			templateId = data['templateId']
			del data['action']
			del data['templateId']
			if not app.db.GetTemplateById(templateId)['ownerId'] == app.db.GetUserByEmail(session['username'])['id']:
				flash('You do not own this template.')
				return redirect(url_for('templates'))

			app.db.UpdateTemplate(templateId, data)
			flash('Template updated.')
			return redirect(url_for('templates'))

		case _:
			flash('Something went wrong.')
			return redirect(url_for('templates'))

@app.route('/deleteTemplate')
@login_required
def deleteTemplate():
	if not request.args.get('id'):
		flash('No ID.')
		return redirect(url_for('templates'))

	template = app.db.GetTemplateById(request.args.get('id'))
	if not template['ownerId'] == app.db.GetUserByEmail(session['username'])['id']:
		flash('You do not own this template.')
		return redirect(url_for('templates'))

	app.db.DeleteTemplateById(request.args.get('id'))
	flash('Template deleted.')
	return redirect(url_for('templates'))
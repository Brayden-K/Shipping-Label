from flask import render_template, jsonify, request, redirect, session, flash, url_for, send_file
from app import app
import requests, datetime, threading, os, glob, re, shutil
from pprint import pprint
from app.decorators import login_required
from app.BTCPayClient import BTCPay
from app.errors import page_not_found, webhook

@app.route('/api', methods=['POST'])
def api():
	if not request.form.get('action'):
		return {'success': False, 'msg': 'No action specified.'}

	match request.form.get('action'):
		case 'checkEmailAvailable':
			if not request.form.get('email'):
				return {'success': False, 'msg': 'No email specified.'}

			email = request.form.get('email')
			if app.db.GetUserByEmail(email):
				return {'success': False, 'msg': 'Email already in use.'}

			return {'success': True, 'msg': 'Email available.'}

		case 'updateSettings':
			data = request.form.to_dict()
			del data['action']
			data['requireCaptcha'] = [1 if data['requireCaptcha'] == 'true' else 0]
			data['underConstruction'] = [1 if data['underConstruction'] == 'true' else 0]
			data['showDashboardMessage'] = [1 if data['showDashboardMessage'] == 'true' else 0]

			app.db.UpdateSettings(data)
			return {'success': True}

		case 'getTemplate':
			data = request.form.to_dict()
			del data['action']
			template = app.db.GetTemplateById(data['id'])
			if template['ownerId'] == app.db.GetUserByEmail(session['username'])['id']:
				return {'success': True, 'template': template}
			else:
				return {'success': False, 'msg': 'You do not own this template.'}

		case 'updateTicket':
			data = request.form.to_dict()
			ticketId = data['id']
			del data['action']
			del data['id']
			app.db.UpdateTicket(ticketId, data)
			return {'success': True}

		case _:
			return {'success': False, 'msg': 'Invalid action specified.'}


@app.route('/api/callback', methods=['POST'])
def callbackapi():
	BTC = BTCPay()
	invoiceId = request.json.get('invoiceId')
	match request.json.get('type'):
		case 'InvoiceSettled':
			invoiceFromDB = app.db.GetInvoiceByInvoiceId(invoiceId)
			invoiceFromBTCPay = BTC.getInvoice(invoiceId)
			if invoiceFromBTCPay['status'] == 'complete' and invoiceFromDB['price'] == invoiceFromBTCPay['price']:
				# UPDATE MYSQL MARK PAID PROJECT AND COMPLETE INVOICES
				app.db.UpdateInvoice(invoiceId, 'complete')
				app.db.UpdateProject(invoiceFromDB['projectId'], {"paid": 1})
				webhook('Invoice Created', f"Invoice ID: {invoiceId} | Price: {invoiceFromBTCPay['price']}\nStatus: {invoiceFromBTCPay['status']}", type='invoice')

		case 'InvoiceInvalid':
			app.db.UpdateInvoice(invoiceId, 'InvoiceInvalid')

		case 'InvoiceExpired':
			app.db.UpdateInvoice(invoiceId, 'InvoiceExpired')

		case 'InvoiceCreated':
			invoice = BTC.getInvoice(invoiceId)
			webhook('Invoice Created', f"Invoice ID: {invoiceId} | Price: {invoice['price']}\nStatus: {invoice['status']}", type='invoice')
	return jsonify('OK')
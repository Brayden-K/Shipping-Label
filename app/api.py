from flask import render_template, jsonify, request, redirect, session, flash, url_for, send_file
from app import app
import requests, datetime, threading, os, glob, re, shutil, base64
from pprint import pprint
from app.decorators import login_required
from app.errors import page_not_found, webhook
from app.labelHandler import createLabel
from io import BytesIO
from PIL import Image

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

		case 'getServices':
			data = request.form.to_dict()
			del data['action']
			services = app.db.GetServices(data['id'])
			return {'success': True, 'services': services}

		case 'changePassword':
			data = request.form.to_dict()
			if not data['currentPassword']:
				return {'success': False, 'msg': 'Current password not specified.'}

			if not data['newPassword']:
				return {'success': False, 'msg': 'New password not specified.'}

			if not data['newRepeatPassword']:
				return {'success': False, 'msg': 'Repeated password not specified.'}

			if not data['newPassword'] == data['newRepeatPassword']:
				return {'success': False, 'msg': 'New passwords do not match.'}

			del data['action']
			current_password = app.db.GetUserByEmail(session['username'])['password']
			if not current_password == data['currentPassword']:
				return {'success': False, 'msg': 'Current password is incorrect.'}

			# Insert new password
			app.db.UpdateUserPassword(session['username'], data['newPassword'])
			return {'success': True}

		case 'saveUserSettings':
			data = request.form.to_dict()
			del data['action']
			if not data.get('email'):
				return {'success': False, 'msg': 'No email specified.'}

			if not data.get('discord'):
				return {'success': False, 'msg': 'No discord specified.'}

			if not data.get('telegram'):
				return {'success': False, 'msg': 'No telegram specified.'}

			app.db.SaveUserSettings(app.db.GetUserByEmail(session['username'])['id'], data)
			session['username'] = data['email']
			return {'success': True}



		case 'createLabel':
			data = request.form.to_dict()
			service = app.db.GetServiceById(data['id'])
			del data['id']
			user = app.db.GetUserByEmail(session['username'])
			if user['balance'] < service['price']:
				return {'success': False, 'msg': 'Not enough credits.'}

			app.db.RemoveBalanceFromUser(session['username'], service['price'])

			match service['provider']:
				case '1':
					labelData = createLabel(data, service, user).createFEDEX()
					if not labelData['Success']:
						app.db.AddBalanceToUser(session['username'], service['price'])
						return {'success': False, 'msg': 'Something went wrong. You have been refunded.'}
					dbData = {
						'ownerId': user['id'],
						'orderId': labelData['orderId'],
						'label': labelData['label'],
						'receipt': None,
						'tracking': labelData['Data']['Order']['Track'],
						'created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
					}

				case '2':
					labelData = createLabel(data, service, user).createUPS()
					if not labelData['success']:
						app.db.AddBalanceToUser(session['username'], service['price'])
						return {'success': False, 'msg': 'Something went wrong. You have been refunded.'}
					dbData = {
						'ownerId': user['id'],
						'orderId': labelData['orderId'],
						'label': rotate_image(labelData['data']['label']),
						'receipt': labelData['data']['receipt'],
						'tracking': labelData['data']['tracking'],
						'created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
					}
	
				case '3':
					labelData = createLabel(data, service, user).createUSPS()
					try:
						text = labelData['Data']['Order']['ID']
					except:
						app.db.AddBalanceToUser(session['username'], service['price'])
						return {'success': False, 'msg': 'Something went wrong. You have been refunded.'}
					dbData = {
						'ownerId': user['id'],
						'orderId': labelData['orderId'],
						'label': labelData['label'],
						'receipt': None,
						'tracking': labelData['Data']['Order']['Track'],
						'created': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
					}

			app.db.Insert('orders', dbData)
			return {'success': True, 'url': url_for('orders')}

		case 'updateTicket':
			data = request.form.to_dict()
			ticketId = data['id']
			del data['action']
			del data['id']
			app.db.UpdateTicket(ticketId, data)
			return {'success': True}

		case _:
			return {'success': False, 'msg': 'Invalid action specified.'}

def rotate_image(base64_image):
	base64_image = 'data:image/png;base64,' + base64_image
	# Decode the base64 image data
	image_data = base64.b64decode(base64_image.split(',')[1])

	# Open the image using PIL
	img = Image.open(BytesIO(image_data))

	# Rotate the image counterclockwise by 90 degrees
	img = img.transpose(method=Image.Transpose.ROTATE_90)

	# Convert the rotated image to a bytes buffer
	buffer = BytesIO()
	img.save(buffer, format="PNG")

	# Encode the rotated image as a base64 string
	rotated_base64 = base64.b64encode(buffer.getvalue()).decode()

	# Return the base64 string of the rotated image
	return rotated_base64
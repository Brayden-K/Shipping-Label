import requests, random, base64, time
from io import BytesIO
from app import app
from pprint import pprint
import pypdfium2 as pdfium

def CreateOrderNumber(digits):
	min_num = 10**(digits-1)  # minimum number that can be generated with the given digits
	max_num = (10**digits)-1  # maximum number that can be generated with the given digits
	return random.randint(min_num, max_num)

class createLabel:
	def __init__(self, data, service, user):
		self.settings = app.db.GetSettings()
		self.data = data
		self.service = service
		self.user = user
		self.orderNumber = CreateOrderNumber(12)

	def createUPS(self):
		url = "https://api.label.supply/v1/label/create"
		signature = True if self.data['signature'] else False
		saturday = True if self.data['saturday'] else False
	
		payload = {
			"uuid": self.settings['upsApiKey'],
			"payload": {
				"serviceName": self.service['name'],
				"fromCustomer": {
					"address1": self.data['fromaddress1'],
					"address2": self.data['fromaddress2'],
					"address3": self.data['fromaddress3'],
					"city": self.data['fromcity'],
					"state": self.data['fromstate'],
					"postalCode": self.data['frompostalCode'],
					"companyName": self.data['fromcompanyName'],
					"phone": self.data['fromphone']
				},
				"toCustomer": {
					"address1": self.data['toaddress1'],
					"address2": self.data['toaddress2'],
					"address3": self.data['toaddress3'],
					"city": self.data['tocity'],
					"state": self.data['tostate'],
					"postalCode": self.data['topostalCode'],
					"companyName": self.data['tocompanyName'],
					"phone": self.data['tophone']
				},
				"pkgInfo": {
					"length":self.data['formlength'],
					"width": self.data['formwidth'],
					"height": self.data['formheight'],
					"weight": self.data['formweight'],
					"description": "details"
				},
				"country": "US",
				"accountNumber": "real",
				"refNumbers": [f"{self.orderNumber}"],
				"signature": signature,
				"saturdayDelivery": saturday
			}
		}
		headers = {"Content-Type": "application/json"}
		
		r = requests.post(url, json=payload, headers=headers)
		
		returnData = r.json()
		returnData['orderId'] = self.orderNumber
		return returnData
	
	def createUSPS(self):
		url = "https://aio.gg/api/uspsv4/order"

		payload = {
			"FromCountry": self.data['fromcountry'],
			"FromName": self.data['fromcompanyName'],
			"FromStreet": self.data['fromaddress1'],
			"FromStreet2": self.data['fromaddress2'],
			"FromCity": self.data['fromcity'],
			"FromState": self.data['fromstate'],
			"FromZip": self.data['frompostalCode'],
			"FromPhone": self.data['fromphone'],
			"ToCountry": self.data['tocountry'],
			"ToName": self.data['tocompanyName'],
			"ToStreet": self.data['toaddress1'],
			"ToStreet2": self.data['toaddress2'],
			"ToCity": self.data['tocity'],
			"ToState": self.data['tostate'],
			"ToZip": self.data['topostalCode'],
			"ToPhone": self.data['tophone'],
			"Weight": self.data['formweight'],
			"Length": self.data['formlength'],
			"Width": self.data['formwidth'],
			"Height": self.data['formheight'],
			"Notes": self.orderNumber,
			"Class": self.service['value']
		}
		headers = {
			"Content-Type": "application/x-www-form-urlencoded",
			"Auth": self.settings['uspsApiKey']
		}
		
		r = requests.post(url, data=payload, headers=headers)
		self.returnData = r.json()
		if not r.json()['Success']:
			if r.json()['Error'] == 'You do not have enough balance':
				print('NOT ENOUGH BALANCE USPS')
			return {'Success': False, 'msg': r.json()['Error']}

		
		self.returnData['orderId'] = self.orderNumber
		self.getLabelImageBytesUSPS()
		return self.returnData
	
	def createFEDEX(self):
		url = "https://aio.gg/api/fedexv3/order"

		payload = {
			"FromCountry": self.data['fromcountry'],
			"FromName": self.data['fromcompanyName'],
			"FromAddress": self.data['fromaddress1'],
			"FromAddress2": self.data['fromaddress2'],
			"FromCity": self.data['fromcity'],
			"FromState": self.data['fromstate'],
			"FromZip": self.data['frompostalCode'],
			"FromPhone": self.data['fromphone'],
			"ToCountry": self.data['tocountry'],
			"ToName": self.data['tocompanyName'],
			"ToAddress": self.data['toaddress1'],
			"ToAddress2": self.data['toaddress2'],
			"ToCity": self.data['tocity'],
			"ToState": self.data['tostate'],
			"ToZip": self.data['topostalCode'],
			"ToPhone": self.data['tophone'],
			"Weight": self.data['formweight'],
			"Length": self.data['formlength'],
			"Width": self.data['formwidth'],
			"Height": self.data['formheight'],
			"Provider": "3",
			"Notes": self.orderNumber,
			"Class": self.service['value']
		}
		headers = {
			"Content-Type": "application/x-www-form-urlencoded",
			"Auth": self.settings['fedexApiKey']
		}
		
		r = requests.post(url, data=payload, headers=headers)
		if not r.json()['Success']:
			if r.json()['Error'] == 'You do not have enough balance':
				print('NOT ENOUGH BALANCE FEDEX')
			return {'Success': False, 'msg': r.json()['Error']}

		self.returnData = r.json()
		self.returnData['orderId'] = self.orderNumber
		self.getLabelImageBytesFedEx()
		return self.returnData

	def getLabelImageBytesFedEx(self):
		orderId = self.returnData['Data']['Order']['ID']

		url = f"https://aio.gg/api/fedexv3/order/{orderId}/file"
		
		headers = {
			"Auth": self.settings['fedexApiKey'],
			"Content-Type": "application/pdf"
		}
		
		response = requests.get(url, headers=headers)
		if response.status_code != 200:
			self.returnData['Success'] = False
			return
		pdf = pdfium.PdfDocument(response.content)
		
		page = pdf.get_page(0)
		image = page.render_topil(
			scale=300/72,
			rotation=0,
			crop=(0, 100, 500, 0),
			greyscale=False,
			optimise_mode=pdfium.OptimiseMode.NONE,
		)
		buffered = BytesIO()
		image.save(buffered, format="PNG")
		img_str = base64.b64encode(buffered.getvalue())
		self.returnData['label'] = img_str

	def getLabelImageBytesUSPS(self):
		orderId = self.returnData['Data']['Order']['ID']

		url = f"https://aio.gg/api/uspsv4/order/{orderId}/file"
		
		headers = {
			"Auth": self.settings['uspsApiKey'],
			"Content-Type": "application/pdf"
		}
		
		while True:
			response = requests.get(url, headers=headers)
			if response.status_code != 200:
				if response.json()["Error"] == 'The order file is not ready':
					print('Not Ready')
					time.sleep(5)
				else:
					self.returnData['Success'] = False
					return
			else:
				break

		pdf = pdfium.PdfDocument(response.content)
		
		page = pdf.get_page(0)
		image = page.render_topil(
			scale=300/72,
			rotation=0,
			crop=(0, 0, 0, 0),
			greyscale=False,
			optimise_mode=pdfium.OptimiseMode.NONE,
		)
		buffered = BytesIO()
		image.save(buffered, format="PNG")
		img_str = base64.b64encode(buffered.getvalue())
		self.returnData['label'] = img_str
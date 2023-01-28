from btcpay import BTCPayClient
import pickle
import pymysql.cursors, time
from pprint import pprint
from app import app
import time

class BTCPay:
	def __init__(self):
		self.client = pickle.loads(app.db.GetBTCPayClient())

	def createInvoice(self, price):
		new_invoice = self.client.create_invoice({"price": price, "currency": "USD", "merchantName": "EdgeDev"})
		ts = time.strftime('%Y-%m-%d %H:%M:%S')
		return new_invoice

	def getInvoice(self, invoiceId):
		return self.client.get_invoice(invoiceId)



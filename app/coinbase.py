from coinbase_commerce.client import Client
from coinbase_commerce.error import WebhookInvalidPayload, SignatureVerificationError
from coinbase_commerce.webhook import Webhook

class Coinbase:
	def __init__(self, key, signingSecret):
		self.client = Client(api_key=key)
		self.signingSecret = signingSecret

	def createInvoice(self, product):
		checkout = {
			'name': product['name'],
			'description': product['description'],
			'local_price': {
				'amount': f"{product['price']}",
				'currency': 'USD'
			},
			'pricing_type': 'fixed_price',
			'redirect_url': product['successUrl'],
			'cancel_url':  product['cancelUrl'],
			'metadata': product['metadata'],
		}
		charge = self.client.charge.create(**checkout)
		redirectUrl = charge['hosted_url']
		return redirectUrl
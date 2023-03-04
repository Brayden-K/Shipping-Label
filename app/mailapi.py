from app import app
import requests

class sendMail:
	def __init__(self, recipient, subject, recoveryLink=None, password=None):
		self.headers = {
			'X-Server-API-Key': app.db.GetSettings()['mailApiKey']
		}
		self.recipient = recipient
		self.subject = subject
		if recoveryLink:
			self.setupSendCode(recoveryLink)
		if password:
			self.setupSendPassword(password)
		self.send()

	def send(self):
		url = "https://kingmailer.org/api/v1/send/message"
		
		payload = {
		    "to": [self.recipient],
		    "cc": "",
		    "bcc": "",
		    "from": "no-reply@cheapship.io",
		    "sender": "Admin",
		    "subject": self.subject,
		    "tag": "",
		    "reply_to": "",
		    "plain_body": self.PLAIN_TEXT,
		    "html_body": self.BODY_HTML,
		    "attachments": "",
		    "headers": "",
		    "bounce": ""
		}

		r = requests.post(url, json=payload, headers=self.headers)
		if r.json()['status'] == 'success':
			return True

	def setupSendCode(self, link):
		self.BODY_HTML = f"<h1>Password Recovery</h1><br>Click this link to recover your password. <a href='{link}'>{link}</a>"
		self.PLAIN_TEXT = f"Password Recovery Click this link to recover your password. {link}"

	def setupSendPassword(self, password):
		self.BODY_HTML = f"<h1>Your new password</h1><br>Your temporary password is here. Please change this ASAP.<br><code>{password}</code>"
		self.PLAIN_TEXT = f"Your new password Your temporary password is here. Please change this ASAP. {password}"

sendMail('direnoho.uderiqi@labworld.org', 'Password Recovery Email', recoveryLink='https://google.com', password=None)
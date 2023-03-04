from app import app
from email.utils import formataddr
from smtplib import SMTP_SSL, SMTPException, SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl

class sendMail:
	def __init__(self, RECIPIENT, subject, recoveryLink=None, password=None):
		self.RECIPIENT = RECIPIENT
		self.subject = subject
		if recoveryLink:
			self.setupSendCode(recoveryLink)
		if password:
			self.setupSendPassword(password)
		self.send()

	def send(self):
		settings = app.db.GetSettings()
		SENDER = settings['emailSender']
		SENDERNAME = settings['emailSenderName']
		
		USERNAME_SMTP = settings['emailUsername']
		
		PASSWORD_SMTP = settings['emailPassword']
		
		HOST = settings['emailHost']
		PORT = settings['emailPort']
		
		# The subject line of the email.
		SUBJECT = self.subject
		
		# The HTML body of the email.
		
		# Create message container - the correct MIME type is multipart/alternative.
		msg = MIMEMultipart('alternative')
		msg['Subject'] = SUBJECT
		msg['From'] = formataddr((SENDERNAME, SENDER))
		msg['To'] = self.RECIPIENT
		# Comment or delete the next line if you are not using a configuration set
		# msg.add_header('X-SES-CONFIGURATION-SET',CONFIGURATION_SET)
		
		msg.attach(MIMEText(self.BODY_HTML, 'html'))
		
		# Try to send the message.
		try:
			context = ssl.SSLContext(ssl.PROTOCOL_TLS)
			with SMTP(HOST, PORT) as server:
				server.starttls(context=context)
				server.login(USERNAME_SMTP, PASSWORD_SMTP)
				server.sendmail(SENDER, self.RECIPIENT, msg.as_string())
				server.close()
				print("Email sent!")
		
		except SMTPException as e:
			print("Error: ", e)

	def setupSendCode(self, link):
		self.BODY_HTML = f"<h1>Password Recovery</h1><br>Click this link to recover your password. <a href='{link}'>{link}</a>"

	def setupSendPassword(self, password):
		self.BODY_HTML = f"<h1>Your new password</h1><br>Your temporary password is here. Please change this ASAP.<br><code>{password}</code>"
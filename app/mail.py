from app import app
from email.utils import formataddr, formatdate, make_msgid
from smtplib import SMTP_SSL, SMTPException, SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl, traceback

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

		msg.add_header('date', formatdate(localtime=True))
		msg.add_header('Message-Id', make_msgid())
		
		msg.attach(MIMEText(self.PLAIN_TEXT, 'plain'))
		msg.attach(MIMEText(self.BODY_HTML, 'html'))
		
		# Try to send the message.
		try:
			context = ssl.create_default_context()
			context.set_ciphers('DEFAULT:!DH')
			with SMTP(HOST, PORT) as server:
				server.starttls(context=context)
				server.login(USERNAME_SMTP, PASSWORD_SMTP)
				print(SENDER, self.RECIPIENT, msg.as_string())
				server.sendmail(SENDER, self.RECIPIENT, msg.as_string())
				server.close()
				print("Email sent!")
		
		except SMTPException as e:
			print("Error: ", e)
			print(traceback.format_exc())

	def setupSendCode(self, link):
		self.BODY_HTML = f"<h1>Password Recovery</h1><br>Click this link to recover your password. <a href='{link}'>{link}</a>"
		self.PLAIN_TEXT = f"Password Recovery Click this link to recover your password. {link}"

	def setupSendPassword(self, password):
		self.BODY_HTML = f"<h1>Your new password</h1><br>Your temporary password is here. Please change this ASAP.<br><code>{password}</code>"
		self.PLAIN_TEXT = f"Your new password Your temporary password is here. Please change this ASAP. {password}"
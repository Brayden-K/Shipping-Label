from app import app
from email.utils import formataddr
from smtplib import SMTP_SSL, SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class sendMail:
	def __init__(self, RECIPIENT, subject, emailType):
		self.RECIPIENT = RECIPIENT
		self.username = username
		self.password = password
		self.subject = subject
		self.emailType = emailType
		self.setupHTML()
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
		SUBJECT = settings['emailSubject']
		
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
		    with SMTP_SSL(HOST, PORT) as server:
		        server.login(USERNAME_SMTP, PASSWORD_SMTP)
		        server.sendmail(SENDER, self.RECIPIENT, msg.as_string())
		        server.close()
		        print("Email sent!")
		
		except SMTPException as e:
		    print("Error: ", e)

	def setupHTML(self):
		self.BODY_HTML = """<h1>Hello</h1>"""
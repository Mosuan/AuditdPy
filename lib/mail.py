#-*- coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from config import *
from log import Log

class Mail(object):

	def __init__(self):
		self.mail_host = mail_host
		self.mail_port = mail_port
		self.mail_user = mail_user
		self.mail_pass = mail_pass
		self.receivers = mail_receivers


	def content(self, msg):
		message = MIMEText(msg, 'html')
		message['from'] = self.mail_user
		message['to'] = self.receivers

		msg = """
	{}
		""".format(msg)
		message['Subject'] = Header(mail_title, 'utf-8')
		return message

	def sendmail(self, msg):
		try:
			message = self.content(msg)
			objs = smtplib.SMTP(self.mail_host, )
			objs.login(self.mail_user, self.mail_pass)
			objs.sendmail(self.mail_user, self.receivers, message.as_string())
			objs.quit()
			return 'done'
		except smtplib.SMTPException, e:
			objs.quit()
			Log().debug("mail.py sendmail error: %s" % (str(e)))
			return 'fail'
			

if __name__ == '__main__':

	obj = Mail()
	print(obj.sendmail("""

auditdPy

auditd log py
ip

ifconfig -a|grep inet|grep -v 127.0.0.1|grep -v inet6 | awk '{print $2}' | tr -d 'addr:'
"""))
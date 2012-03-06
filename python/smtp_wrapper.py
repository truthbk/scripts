#!/usr/bin/python3
#
# Simple reusable class to wrap smtp python functions

import smtplib

class MyMailer:
#	Name = "MyMailer"

	def __init__(self, smtpserver=None, smtpport=None, smtpuser=None, smtppass=None, from_address=None, to_address=None):
		self.toaddr= to_address
		self.fromaddr = from_address
		self.authuser = smtpuser
		self.authpasswd = smtppass
		self.server = smtplib.SMTP(smtpserver, smtpport)

	def set_fromaddr(self, fromaddr):
		self.fromaddr = fromaddr
	
	def set_toaddr(self, toaddr):
		self.toaddr = toaddr
	
	def set_smtpserver(self, smtpserver):
		self.smtpserver = smtpserver
		self.server = server.smtplib.SMTP(self.smtpserver, self.smtpport)
	
	def set_smtpport(self, smtpport):
		self.smtpport = smtpport
		self.server = server.smtplib.SMTP(self.smtpserver, self.smtpport)

	def login(self):
		self.server.ehlo()
		self.server.starttls()
		self.server.login(self.authuser,self.authpasswd)

	def send_message(self, msg):
		self.login()
		self.server.sendmail(self.fromaddr, self.toaddr,msg)
		self.server.quit()
		

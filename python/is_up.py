#!/usr/bin/python3
#
# Script to check if supplied argument url is up. 
# If not, an email to the supplied address is sent.

import getopt
import re
import sys
from email.mime.text import MIMEText
from my_shellcmd import ShellCmdClass
from smtp_wrapper import MyMailer

def usage():
	print('usage:\n%s [-u url] [-m email] [-s smtpserver] [-p smtpport] [-f fromemail]\n' % (sys.argv[0]))

def main(argv):
	email = ""
	url = ""
	smtpserv = ""
	smtpport = ""
	fromemail = ""
	smtpuser="truthbk@gmail.com"
	smtppass="1979noemi"

	try:
		opts, args = getopt.getopt(argv, "hu:m:s:f:p:", ["help", "url=","mail=","smtp=","frommail=","port="])
	except getopt.GetoptError:
		usage()
		exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			exit(2)
		elif opt in ("-u", "--url"):
			url = arg
		elif opt in ("-m", "--mail"):
			email = arg
		elif opt in ("-s", "--smtp"):
			smtpserv = arg
		elif opt in ("-p", "--port"):
			smtpport = int(arg)
		elif opt in ("-f", "--frommail"):
			fromemail = arg
	
	#vars should be verified to be non-empty and correctly entered
	#ie.	addr@mail.com for emails
	#	smtp.someserver.com for hosts
	#
	#	xxx.xxx.xxx.xxx
	#	some.url.com	for urls



	my_mailer = MyMailer(smtpserv, smtpport, smtpuser, smtppass, fromemail, email)
	ping_cmd = ShellCmdClass(["ping", "-c4", url]);
	ping_out = ping_cmd.runcmd_chkoutput()
	ping_out_str = ping_out.decode("utf-8")

	m = re.search('([0-9] received)',ping_out_str)
	stats = re.split('\s',m.group(0))

	if int(stats[0]) == 0:
		msg = MIMEText('The server at URL: %s, appears to be down!\nPlease notify the webmaster.\n' % (url) )
		msg['Subject']='%s is Down' % (url)
		msg['From']=fromemail
		msg['To']=email
		my_mailer.send_message(msg.as_string())


if __name__ == "__main__":
	main(sys.argv[1:])

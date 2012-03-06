#!/usr/bin/python

import urllib
import urllib2
import cookielib
import getopt
import sys

def getRandHTMLResponse(response):
	target = "<form id=\'login"
	targetresponse = "<div id=\'loginbox\'"
	
	response = response[response.find(targetresponse):len(response)]
	return response[response.find(target)+len(target):response.find(target)+len(target):response.find(target)+len(target)+4]

def getHiddenRandHTMLResponse(response):
	target = "<input type=\'hidden\' name=\'multiform\' value=\'"
	targetresponse = "<div id=\'loginbox\'"
	parsedres = response[response.find(targetresponse):len(response)]
	return parsedres[parsedres.find(target)+len(target):parsedres.find(target)+len(target)+34]


def checkLogin(response):
	target = "<title>DynDNS.com - My Account</title>"
	if response.find(target) == -1:
		return False
	return True


class HTMLSession:
	cj = None
	opener = None
	txHeaders = None

	def __init__(self, txHeaders):
		#The CookieJar will hold any cookies necessary throughout the login process.
		self.cj = cookielib.MozillaCookieJar()
		self.txHeaders = txHeaders
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        	urllib2.install_opener(self.opener)

	def setHeaders(self, txheaders):
		self.txHeaders = txHeaders
	
	def getHeaders(self):
		return self.txHeaders
	
	def openURI(self, uri, txdata):
		try:
			req = urllib2.Request(uri, txdata, self.txHeaders)
			# create a request object
	
			handle = urllib2.urlopen(req)
			# and open it to return a handle on the url

		except IOError as e:
			print 'we failed to open "%s".' % uri

			if hasattr(e, 'code'):
				print 'We failed with error code - %s.' % e.code
			elif hasattr(e, 'reason'):
				print "The error object has the following 'reason' attribute :"
				print e.reason
				print "This usually means the server doesn't exist,'"
				print "is down, or we don't have an internet connection."
				return None
		else:
			return handle.read()


def main(argv):
	username = ""
	password = ""
	hiddenval = ""
	theurl = "https://www.dyndns.com/account/entrance/"
	thelogouturl = "https://www.dyndns.com/account/entrance/?__logout=1"
	txdata = None
	txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
	# fake a user agent, some websites (like google) don't like automated exploration


	try:

		opts, args = getopt.getopt(argv, "hu:p:", ["help", "username=","password="])
	except getopt.GetoptError:
		usage()
		exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			exit(2)
		elif opt in ("-u", "--username"):
			username = arg
		elif opt in ("-p", "--password"):
			password = arg

	myhtmlsession = HTMLSession(txheaders)
	response = myhtmlsession.openURI(theurl, None)
	
	if response == None:
		sys.exit(0)
	
	hiddenval = getHiddenRandHTMLResponse(response)
	txdata = urllib.urlencode({'username':username, 'password':password, 'multiform':hiddenval, 'submit': "Log in"})
	
	response = myhtmlsession.openURI(theurl, txdata)
	if response == None:
		sys.exit(0)

	#we should sleep here for about 10 seconds.
	if checkLogin(response):
		print('We have succesfully logged into DynDNS.')

	response = myhtmlsession.openURI(thelogouturl, None)
	if response == None:
		sys.exit(0)


if __name__ == "__main__":
	main(sys.argv[1:])

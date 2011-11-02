#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: opener.py

import urllib2,cookielib
import random

global_custom_opener_installed = False

def newOpenerWithCookie():
	cookie = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
	agents = ["Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)","Internet Explorer 7 (Windows Vista); Mozilla/4.0 ","Google Chrome 0.2.149.29 (Windows XP)","Opera 9.25 (Windows Vista)","Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)","Opera/8.00 (Windows NT 5.1; U; en)"]
	agent = random.choice(agents)
	opener.addheaders=[('User-agent',agent)]
	return opener

def installOpenerWithCookie():
	global global_custom_opener_installed
	if not global_custom_opener_installed:
		opener = newOpenerWithCookie()
		urllib2.install_opener(opener)
		global_custom_opener_installed = True


class OpenerManager:
	def __init__(self):
		self.dict = {}
	
	def get_openner(self, site, user):
		host = 'localhost'
		key = (host, user)
		if self.dict.has_key(key):
			return self.dict[key]
		opener = newOpenerWithCookie()
		self.dict[key] = opener
		return opener

opener_mgr = OpenerManager()
def getOpener(site, user):
	return opener_mgr.get_openner(site, user)
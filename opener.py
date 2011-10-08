#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: opener.py

import urllib2,cookielib
import random

global_custom_opener = None
global_custom_opener_installed = False

def getOpenerWithCookie():
	global global_custom_opener
	if global_custom_opener is None:
		cookie = cookielib.CookieJar()
		global_custom_opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		agents = ["Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)","Internet Explorer 7 (Windows Vista); Mozilla/4.0 ","Google Chrome 0.2.149.29 (Windows XP)","Opera 9.25 (Windows Vista)","Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)","Opera/8.00 (Windows NT 5.1; U; en)"]
		agent = random.choice(agents)
		global_custom_opener.addheaders=[('User-agent',agent)]
	return global_custom_opener

def installOpenerWithCookie():
	global global_custom_opener_installed
	if not global_custom_opener_installed:
		opener = getOpenerWithCookie()
		urllib2.install_opener(opener)
		global_custom_opener_installed = True

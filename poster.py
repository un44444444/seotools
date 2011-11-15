#!/usr/bin/env python
# encoding: UTF-8

import urllib,urllib2

def post_data(action, data):
	#try:
		#data = urllib.urlencode(data)
		req=urllib2.Request(action,data)
		resp=urllib2.urlopen(req)
		content=resp.read()
		return content
	#except:
	#	return 'except'

if __name__ == '__main__':
	action = 'http://api.spinnerchief.com:8080/?apikey=45a0a23babbd44729&username=un44444444&password=44444444'
	print action
	data = 'Hello, what is your name?'
	result = post_data(action, data)
	print result

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

def get_data(action):
	#try:
		req=urllib2.Request(action)
		resp=urllib2.urlopen(req)
		content=resp.read()
		return content
	#except:
	#	return 'except'

if __name__ == '__main__':
	apikey = '45a0a23babbd44729'
	username = 'un44444444'
	password = '44444444'
	action = 'http://api.spinnerchief.com:9001/?apikey=%s&username=%s&password=%s' % (apikey, username, password)
	action = action + '&spintype=1&spinfreq=1&original=1'
	#action = action + '&querytimes=2'
	print action
	data = "Because of cubic zirconia's low cost, high quality, and close visual likeness to diamond, cubic zirconia is also known as cz, zirconia and man made diamonds, the best substitute of natural diamonds. synthetic cubic zirconia has remained the most gemologically and economically important competitor for diamonds since 1976.shoponchina is the direct factory sources for cubic zirconia, We have over 25 years of experience in the cubic zirconia wholesale business. Our value is our knowledge and tenure in helping our customers succeed."
	#data = ''
	result = post_data(action, data)
	print result

#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: http.py

import urllib,urllib2
import time
import opener

class HttpClient:
	def __init__(self, site, user):
		self.opener = opener.getOpener(site, user)
		#opener.installOpenerWithCookie()

	def request_get(self, action, referer='', retry_count=5):
		req=urllib2.Request(action)
		if referer:
			req.add_header('Referer', referer)
		content = ""
		err_count = 0
		flag = True
		while flag:
			try:
				#u=urllib2.urlopen(req)
				u=self.opener.open(req)
				content=u.read()
				flag=False
			except urllib2.HTTPError, e:
				if err_count > retry_count:
					exit(1)
				err_count += 1
				print e
				flag = True
				if e.getcode()== 403:
					print "Wait for 5 minutes..."
					time.sleep(5 * 60)
		#return content
		return content

	def request_get_simple(self, action, referer=''):
		req=urllib2.Request(action)
		if referer:
			req.add_header('Referer', referer)
		#u=urllib2.urlopen(req)
		u=self.opener.open(req)
		content=u.read()
		return content

	def request_post(self, action, data, referer='', retry_count=5):
		if isinstance(data, basestring):
			post_data = data
		else:
			post_data = urllib.urlencode(data)
		req=urllib2.Request(action,post_data)
		if referer:
			req.add_header('Referer', referer)
		content = ""
		err_count = 0
		flag = True
		while flag:
			try:
				#u=urllib2.urlopen(req)
				u=self.opener.open(req)
				content=u.read()
				flag=False
			except urllib2.HTTPError, e:
				if err_count > retry_count:
					exit(1)
				err_count += 1
				print e
				flag = True
				if e.getcode()== 403:
					print "Wait for 5 minutes..."
					time.sleep(5 * 60)
		#return content
		return content

	def request_post_simple(self, action, data, referer=''):
		if isinstance(data, basestring):
			post_data = data
		else:
			post_data = urllib.urlencode(data)
		req=urllib2.Request(action,post_data)
		if referer:
			req.add_header('Referer', referer)
		#u=urllib2.urlopen(req)
		u=self.opener.open(req)
		content=u.read()
		return content

	def post_then_fetch_url(self, action, data, referer='', retry_count=5):
		request=urllib2.Request(action,urllib.urlencode(data))
		if referer:
			request.add_header('Referer', referer)
		content = ""
		err_count = 0
		flag = True
		while flag:
			try:
				#response=urllib2.urlopen(request)
				response=self.opener.open(request)
				#
				status_code=response.getcode()
				print status_code
				if status_code==301 or status_code==302:
					http_message=response.info()
					print http_message
					content=http_message.getheader('location', 'can not find location')
					return content
				#
				url=response.geturl()
				print url
				if url != action:
					return url
				#
				content=response.read()
				flag=False
			except urllib2.HTTPError, e:
				if err_count > retry_count:
					exit(1)
				err_count += 1
				print e
				flag = True
				if e.getcode()== 403:
					print "Wait for 5 minutes..."
					time.sleep(5 * 60)
		#return content
		return content


if __name__ == "__main__":
	pass

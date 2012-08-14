#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: discuz.py

import urllib,urllib2
import re,time
import opener

class DiscuzBase:
	def __init__(self):
		conf = self.conf
		self.opener = opener.getOpener(conf['url'], conf['username'])
		#opener.installOpenerWithCookie()

	def request_get(self, action, referer='', retry_count=5):
		req=urllib2.Request(action)
		if referer:
			req.add_header('Referer', referer)
		content = ""
		err_count = 0
		flage = True
		while flage:
			try:
				#u=urllib2.urlopen(req)
				u=self.opener.open(req)
				content=u.read()
				flage=False
			except urllib2.HTTPError, e:
				if err_count > retry_count:
					exit(1)
				err_count += 1
				print e
				flage = True
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
		flage = True
		while flage:
			try:
				#u=urllib2.urlopen(req)
				u=self.opener.open(req)
				content=u.read()
				flage=False
			except urllib2.HTTPError, e:
				if err_count > retry_count:
					exit(1)
				err_count += 1
				print e
				flage = True
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
		flage = True
		while flage:
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
				flage=False
			except urllib2.HTTPError, e:
				if err_count > retry_count:
					exit(1)
				err_count += 1
				print e
				flage = True
				if e.getcode()== 403:
					print "Wait for 5 minutes..."
					time.sleep(5 * 60)
		#return content
		return content

	def get_error_message(self,content):
		p = re.compile('<div\s*id="messagetext"\s*class="alert_error"\s*>\s*<p>(.*?)\s*<script\s*')
		m = p.findall(content)
		if len(m) > 0:
			#for i in m:
			#	print  i.replace('</p>','').decode(self.encoding,'ignore')
			return m[0].replace('</p>','')
		else:
			return ''


if __name__ == "__main__":
	pass

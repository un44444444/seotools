#!/usr/bin/env python
# encoding: UTF-8

import webbrowser
import handler

class OpenLusongsong(handler.HandlerBase):
	def __init__(self, name=None):
		handler.HandlerBase.__init__(self, name = name)
		self.prefix = 'http://luson'+'gsong.com'
		self.postfix = ''
		self.time = 30
	
	def deal_a_site(self, site, time=20):
		dest_url = '%s/tool/seo/seo.asp?url=%s&auto=yes&ttime=%d%s' % (self.prefix, site, time, self.postfix)
		webbrowser.open_new_tab(dest_url)
	
	def handle(self, line):
		link=line.split('\t')[0]
		#link=link[:-1].replace('http://', '')
		#url = link.split('/')[0]
		url=link.split(',')[0]
		if url[-1] == '\n':
			url = url[:-1]
		site = url
		self.deal_a_site(site, self.time)
		return '%s, OK'%site
	
if __name__ == '__main__':
	poster = OpenLusongsong('23')
	result=poster.deal_a_site('www.chen-w.com')
	print result
	exit(0)
	poster.prepare_file('R:/input.txt')
	print 'start thread..'
	poster.start()
	print 'wait thread complete ..'
	poster.join()

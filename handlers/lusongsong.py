#!/usr/bin/env python
# encoding: UTF-8
import os
import time
import webbrowser
import handler

class OpenLusongsong(handler.HandlerBase):
	def __init__(self, name=None):
		handler.HandlerBase.__init__(self, name = name)
		self.prefix = 'http://tool.'+'luson'+'gsong.com'
		self.postfix = ''
		self.time = 20
		self.concurrent = 5
		self.waitcomplete = 17*60
	
	def deal_a_site(self, site, ttime=20):
		dest_url = '%s/seo/seo.asp?url=%s&auto=yes&ttime=%d%s' % (self.prefix, site, ttime, self.postfix)
		webbrowser.open_new_tab(dest_url)
		time.sleep(0.5)
	
	def handle(self, line):
		link=line.strip()
		if len(link) <= 3:
			return 'too short'
		link=link.replace('http://', '')
		site = link.split('/')[0]
		if site[-1] == '\n':
			site = site[:-1]
		# 
		if self.total_count%self.concurrent==0 and self.total_count>0:
			time.sleep(self.waitcomplete)
			os.system('taskkill /F /IM iexplore.exe')
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

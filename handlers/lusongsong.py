#!/usr/bin/env python
# encoding: UTF-8
import os
import time
import webbrowser
import handler

import sys
sys.path.append('..')
from common.config import config

class OpenLusongsong(handler.HandlerBase):
	def __init__(self, name=None):
		handler.HandlerBase.__init__(self, name = name)
		self.prefix = 'http://tool.'+'luson'+'gsong.com'
		self.postfix = ''
		self.dealed_count = 0
		self.time = int(config.lusongsong.time) #@UndefinedVariable
		self.concurrent = int(config.lusongsong.concurrent) #@UndefinedVariable
		self.waitcomplete = int(config.lusongsong.waitcomplete) #@UndefinedVariable
	
	def deal_a_site(self, site, ttime=20):
		dest_url = '%s/seo/seo.asp?url=%s&auto=yes&ttime=%d%s' % (self.prefix, site, ttime, self.postfix)
		webbrowser.open_new_tab(dest_url)
		if self.dealed_count%self.concurrent==0:
			time.sleep(5)
		else:
			time.sleep(1.5)
	
	def handle(self, line):
		link=line.strip()
		if len(link) <= 3:
			return 'too short'
		link=link.replace('http://', '')
		site = link.split('/')[0]
		if site[-1] == '\n':
			site = site[:-1]
		# 
		if self.dealed_count%self.concurrent==0 and self.dealed_count>0:
			time.sleep(self.waitcomplete)
			os.system('taskkill /F /IM iexplore.exe')
			os.system('taskkill /F /IM theworld.exe')
		self.deal_a_site(site, self.time)
		self.dealed_count += 1
		return '%s, OK'%site
	
	def run(self):
		self.status = 1
		while self.status == 1:
			self.total_count = 0
			ret = self.deal_file(self.input_file, self.output_file)
			self.reset_offset(self.input_file)
		self.status = 0
		return ret
	def reset_offset(self, in_file):
		tempfilename=in_file+'.offset'
		ftemp=open(tempfilename, 'w')
		ftemp.write('0')
		ftemp.close()
	
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

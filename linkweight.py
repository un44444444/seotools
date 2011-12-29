#!/usr/bin/env python
# encoding: UTF-8

import urllib2
import re
import time

class GetLinkWeight:
	def __init__(self):
		self.site_base = 'http://www.ai' + 'zhan.com'
		self.site_baidu = self.site_base + '/baidu'
		
	def get_weight(self, link):
		main_page = self.site_baidu+'/'+link+'/position/'
		page = self._get_data(main_page, self.site_baidu)
		#
		weight = 'NULL'
		str_re='<td\scolspan="5"\salign="left"><img\ssrc="http:\/\/static.aizhan.com\/images\/brs\/([0-9]*).gif"'
		reObj=re.compile(str_re)
		allMatch=reObj.findall(page)
		if len(allMatch) == 1:
			weight = allMatch[0]
		#
		src1 = src2 = 'NULL'
		str_re='<span class="red">([0-9]*) ~ ([0-9]*)<\/span>'
		reObj=re.compile(str_re)
		allMatch=reObj.findall(page)
		if len(allMatch) == 1:
			(src1, src2) = allMatch[0]
		#
		words = 'NULL'
		str_re='<td colspan="5"\salign="left"><span\sclass="red">([0-9]*)<\/span>'
		reObj=re.compile(str_re)
		allMatch=reObj.findall(page)
		if len(allMatch) == 1:
			words = allMatch[0]
		#
		timestamp = time.time()
		url1 = '/ajaxAction/get.php?domain=%s&action=baidu%%3Ashoulu%%3Aall&n=0&rn=_%d0' % (link, timestamp)
		total_sum = self._get_data2(self.site_base+url1, main_page)
		url2 = '/ajaxAction/get.php?domain=%s&action=baidu%%3Ashoulu%%3A7days&n=0&rn=_%d0' % (link, timestamp)
		week_count = self._get_data2(self.site_base+url2, main_page)
		url3 = '/ajaxAction/get.php?domain=%s&action=baidu%%3Ashoulu%%3A1days&n=0&rn=_%d0' % (link, timestamp)
		day_count = self._get_data2(self.site_base+url3, main_page)
		#
		return (weight,src1,src2,words,total_sum,week_count,day_count)
	
	@staticmethod
	def _get_data(action, referer):
		try:
			req=urllib2.Request(action)
			req.add_header('Referer', referer)
			resp=urllib2.urlopen(req)
			content=resp.read()
			return content
		except:
			return 'except'
	
	@staticmethod
	def _get_data2(action, referer):
		try:
			req=urllib2.Request(action)
			req.add_header('Referer', referer)
			req.add_header('X-Requested-With', 'XMLHttpRequest')
			resp=urllib2.urlopen(req)
			content=resp.read()
			return content
		except:
			return 'except'
	
	def deal_file(self, dir):
		f=open(dir+'/input.txt')
		output=open(dir+'/output.txt', 'w')
		lines=f.readlines()
		for line in lines:
			link=line.split('\t')[0]
			site = link[7:].split('/')[0]
			result = self.get_weight(site)
			print result
			output.write('\t'.join(result) + '\n')
			output.flush()
	
if __name__ == '__main__':
	poster = GetLinkWeight()
	poster.deal_file('R:')
#	result = poster.get_weight('www.10086.cn')
#	print result

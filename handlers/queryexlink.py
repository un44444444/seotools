#!/usr/bin/env python
# encoding: UTF-8

import urllib
import urllib2
import re

import handler
import sys
sys.path.append('..')
from common import opener

class QueryExternalLink(handler.HandlerBase):
	def __init__(self, name=None):
		handler.HandlerBase.__init__(self, name = name)
		self.site_base = 'http://www.bai' + 'du.com'
		self.opener = opener.getOpener(self.site_base, name)
		self.output_header = '查询网址,百度收录'
	
	def query_link(self, link):
		main_page = self.site_base+'/s?wd='+urllib.quote_plus(link)+'&rsv_bp=0&rsv_spt=3&rsv_n=2&inputT=1000'
		page = self._get_data(main_page, self.site_base)
		#
		weight = 'NULL'
		if len(page)<=7:
			weight = 'timeout'
		else:
			# check encoding
			encoding = 'gbk'
			str_re='"text/html;charset=([1-9a-zA-Z-]+)"'
			reObj=re.compile(str_re)
			allMatch=reObj.findall(page)
			if len(allMatch) >= 1:
				encoding = allMatch[0]
			print encoding
			# find key word
			str_re='<span class="nums"([^<]*<)\/span>'
			reObj=re.compile(str_re)
			allMatch=reObj.findall(page)
			#print page
			print allMatch
			# normal
			if len(allMatch) >= 1:
				weight = allMatch[0]
				str_re='.*>(.*)<'
				reObj=re.compile(str_re)
				allMatch=reObj.findall(weight)
				if len(allMatch) >= 1:
					weight = allMatch[0]
				if encoding=='utf-8' or encoding=='UTF-8':
					weight = weight.decode('utf-8').encode('gbk')
				#elif encoding=='gbk' or encoding=='GBK':
				#	weight = weight.decode('gbk').encode('utf-8')
				weight = weight.replace(',', '')
				#print weight
			else:
				str_re='<div class="nors">'
				reObj=re.compile(str_re)
				allMatch=reObj.findall(page)
				if len(allMatch) >= 1:
					weight = 'no result'
		#
		return (link,weight)
	
	def _get_data(self, action, referer, timeout=30):
		try:
			req=urllib2.Request(action)
			req.add_header('Referer', referer)
			resp=self.opener.open(req, timeout=timeout)
			content=resp.read()
			return content
		except:
			return 'except'
	
	def _get_data2(self, action, referer, timeout=30):
		try:
			req=urllib2.Request(action)
			req.add_header('Referer', referer)
			req.add_header('X-Requested-With', 'XMLHttpRequest')
			resp=self.opener.open(req, timeout=timeout)
			content=resp.read()
			return content
		except:
			return 'except'
	
	def handle(self, line):
		link=line.split('\t')[0]
		#link=link[:-1].replace('http://', '')
		#url = link.split('/')[0]
		url=link.split(',')[0]
		if url[-1] == '\n':
			url = url[:-1]
		if len(url)<5:
			result = (url,'TOO SHORT')
		else:
			url=url.replace('"', '')
			result = self.query_link(url)
		print result
		if result[1] == 'NULL':
			self.lasterror = 'ERROR'
		record=','.join(result).replace('##',',')
		return record
	
if __name__ == '__main__':
	poster = QueryExternalLink('23')
	result=poster.query_link('http://detail.zol.com.cn/digital_tv/index56028.shtml')
	print result
	exit(0)
	poster.prepare_file('R:/input.txt', 'R:/output.csv')
#	poster.deal_file('R:/input.txt', 'R:/output.csv')
	print 'start thread..'
	poster.start()
	print 'wait thread complete ..'
	poster.join()
#	result = poster.query_link('www.10086.cn')
#	print result

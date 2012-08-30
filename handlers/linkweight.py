#!/usr/bin/env python
# encoding: UTF-8

import urllib2
import time
import re

import handler
import sys
sys.path.append('..')
from common import opener

class GetLinkWeight(handler.HandlerBase):
	def __init__(self, name=None):
		handler.HandlerBase.__init__(self, name = name)
		self.site_base = 'http://www.ai' + 'zhan.com'
		self.site_baidu = self.site_base + '/baidu'
		self.opener = opener.getOpener(self.site_base, name)
		self.output_header = '百度权重,百度来路,百度来路,爱站词数,网站,总收录,百度快照,一周收录,24小时收录'
		
	def get_weight(self, link):
		main_page = self.site_baidu+'/'+link+'/position/'
		page = self._get_data(main_page, self.site_baidu)
		#
		weight = 'NULL'
		src1 = src2 = 'NULL'
		words = 'NULL'
		if len(page)<=7:
			weight = 'timeout'
		else:
			str_re='<td\scolspan="5"\salign="left"><img\ssrc="http:\/\/static.aizhan.com\/images\/brs\/([0-9]*).gif"'
			reObj=re.compile(str_re)
			allMatch=reObj.findall(page)
			# normal
			if len(allMatch) == 1:
				weight = allMatch[0]
				#
				str_re='<span class="red">([0-9]*) ~ ([0-9]*)<\/span>'
				reObj=re.compile(str_re)
				allMatch=reObj.findall(page)
				if len(allMatch) == 1:
					(src1, src2) = allMatch[0]
				#
				str_re='<td colspan="5"\salign="left"><span\sclass="red">([0-9]*)<\/span>'
				reObj=re.compile(str_re)
				allMatch=reObj.findall(page)
				if len(allMatch) == 1:
					words = allMatch[0]
			# not expect condition
			else:
				str_re='<span style="font-size:14px;">(.*)<\/span>'
				reObj=re.compile(str_re)
				allMatch=reObj.findall(page)
				if len(allMatch) == 1:
					weight = 'error'
					src1 = allMatch[0]
					if len(src1)>=57:
						weight = 'NULL'
					src1 = src1.decode('utf-8').encode('gbk')
					print src1
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
			link=link[:-1].replace('http://', '')
			site = link.split('/')[0]
			result = self.get_weight(site)
			print result
			if result[0] == 'NULL':
				self.lasterror = result[1]
			record=','.join(result).replace('##',',')
			return record
	
	def login(self, email, word):
		data='r=&email=%s&password=%s' % (email,word)
		action_login = self.site_base + '/login.php'
		req=urllib2.Request(action_login,data)
		req.add_header('Referer', action_login)
		u=self.opener.open(req)
		content=u.read()
		return content
	
if __name__ == '__main__':
	poster = GetLinkWeight('23')
	result=poster.get_weight('http://detail.zol.com.cn/digital_tv/index56028.shtml')
	print result
	exit(0)
	poster.prepare_file('R:/input.txt', 'R:/output.csv')
	poster.login('un'+'44444444@yahoo'+'.com', '4444'+'4444')
#	poster.deal_file('R:/input.txt', 'R:/output.csv')
	print 'start thread..'
	poster.start()
	print 'wait thread complete ..'
	poster.join()
#	result = poster.get_weight('www.10086.cn')
#	print result

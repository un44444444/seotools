#!/usr/bin/env python
# encoding: UTF-8

import urllib2
import re,time
import opener
import os
import threading
import codecs

class GetLinkWeight(threading.Thread):
	def __init__(self, name=None):
		if name is None or not name:
			name = str(int(time.time()))
		threading.Thread.__init__(self, name = name)
		self.site_base = 'http://www.ai' + 'zhan.com'
		self.site_baidu = self.site_base + '/baidu'
		self.opener = opener.getOpener(self.site_base, name)
		self.total_count = 0
		self.status = 0
		self.lasterror = '任务未开始。'
		
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
	
	def deal_file(self, in_file, out_file):
		self.status = 1
		self.lasterror = '成功完成。'
		f=open(in_file)
		bom=f.read(3)
		if bom==codecs.BOM_UTF8:
			f.seek(3)
		else:
			f.seek(0)
		tempfilename=in_file+'.offset'
		output=None
		last_offset=0
		# restart from last read
		if os.path.isfile(tempfilename):
			ftemp=open(tempfilename)
			last_offset=int(ftemp.read())
			ftemp.close()
		if last_offset > 0:
			f.seek(last_offset)
			output=open(out_file, 'a')
		else:
			output=open(out_file, 'w')
			output.write('百度权重,百度来路,百度来路,爱站词数,网站,总收录,百度快照,一周收录,24小时收录\n'.decode('utf-8').encode('gbk'))
			output.flush()
		# deal
		dealed_count=0
		while True:
			line=f.readline()
			if not line:
				break
			link=line.split('\t')[0]
			link=link[:-1].replace('http://', '')
			site = link.split('/')[0]
			result = self.get_weight(site)
			print result
			if result[0] == 'NULL':
				dealed_count=0
				self.lasterror = result[1]
			else:
				record=','.join(result).replace('##',',')
				output.write(record + '\n')
				dealed_count+=1
				self.total_count+=1
				last_offset=f.tell()
			# record result
			if dealed_count%10 == 0:
				ftemp=open(tempfilename, 'w')
				ftemp.write(str(last_offset))
				ftemp.close()
				output.flush()
			if dealed_count == 0:
				print self.lasterror
				self.lasterror = self.lasterror.decode('gbk').encode('utf-8')
				break
		#
		self.status = 0
		ftemp=open(tempfilename, 'w')
		ftemp.write(str(last_offset))
		ftemp.close()
	
	def prepare_file(self, in_file, out_file):
		self.input_file=in_file
		self.output_file=out_file
	
	def run(self):
		return self.deal_file(self.input_file, self.output_file)
	
	def get_status(self):
		return self.status
	def get_lasterror(self):
		return self.lasterror
	def get_totalcount(self):
		return self.total_count
	def get_filecount(self):
		#
		infile_count=0
		f=open(self.input_file)
		lines=f.readlines()
		infile_count=len(lines)
		f.close
		#
		outfile_count=0
		f=open(self.output_file)
		lines=f.readlines()
		outfile_count=len(lines)-1
		f.close
		#
		return (infile_count,outfile_count)
	
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
	poster.prepare_file('R:/input.txt', 'R:/output.csv')
	poster.login('un'+'44444444@yahoo'+'.com', '4444'+'4444')
#	poster.deal_file('R:/input.txt', 'R:/output.csv')
	print 'start thread..'
	poster.start()
	print 'wait thread complete ..'
	poster.join()
#	result = poster.get_weight('www.10086.cn')
#	print result

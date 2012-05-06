#!/usr/bin/env python
# encoding: UTF-8

import urllib
import urllib2
import re,time
import opener
import os
import threading
import codecs

class QueryExternalLink(threading.Thread):
	def __init__(self, name=None):
		if name is None or not name:
			name = str(int(time.time()))
		threading.Thread.__init__(self, name = name)
		self.site_base = 'http://www.bai' + 'du.com'
		self.opener = opener.getOpener(self.site_base, name)
		self.total_count = 0
		self.status = 0
		self.lasterror = '任务未开始。'
		
	def get_weight(self, link):
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
	
	def deal_file(self, in_file, out_file):
		self.status = 1
		self.lasterror = '成功完成。'
		f=open(in_file)
		bom=f.read(4)
		other_encoding = [codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE, codecs.BOM_UTF32_LE, codecs.BOM_UTF32_BE]
		if (bom[:2] in other_encoding) or (bom in other_encoding):
			self.status = 0
			self.lasterror = '文件编码无法处理，请另存为UTF-8格式。'
			return
		if bom[:3]==codecs.BOM_UTF8:
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
			output.write('查询网址,百度收录\n'.decode('utf-8').encode('gbk'))
			output.flush()
		# deal
		dealed_count=0
		while True:
			line=f.readline()
			if not line:
				break
			link=line.split('\t')[0]
			#link=link[:-1].replace('http://', '')
			#site = link.split('/')[0]
			site=link.split(',')[0]
			if site[-1] == '\n':
				site = site[:-1]
			if len(site)<5:
				continue
			result = self.get_weight(site)
			print result
			if result[1] == 'NULL':
				dealed_count=0
				#self.lasterror = result[2]
				self.lasterror = 'ERROR'
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
	
if __name__ == '__main__':
	poster = QueryExternalLink('23')
	result=poster.get_weight('http://detail.zol.com.cn/digital_tv/index56028.shtml')
	print result
	exit(0)
	poster.prepare_file('R:/input.txt', 'R:/output.csv')
#	poster.deal_file('R:/input.txt', 'R:/output.csv')
	print 'start thread..'
	poster.start()
	print 'wait thread complete ..'
	poster.join()
#	result = poster.get_weight('www.10086.cn')
#	print result

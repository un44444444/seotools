#!/usr/bin/env python
# encoding: UTF-8

import time
import os
import threading
import codecs

class HandlerBase(threading.Thread):
	def __init__(self, name=None):
		if name is None or not name:
			name = str(int(time.time()))
		threading.Thread.__init__(self, name = name)
		self.total_count = 0
		self.status = 0
		self.lasterror = '任务未开始。'
		self.output_header = 'status,echo'
	
	def handle(self, line):
		return "1,%s" % (line[:-1])
	
	def deal_file(self, in_file, out_file):
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
		# out file
		if out_file:
			if last_offset > 0:
				f.seek(last_offset)
				output=open(out_file, 'a')
			else:
				output=open(out_file, 'w')
				output.write(self.output_header.decode('utf-8').encode('gbk'))
				output.write('\n')
				output.flush()
		# deal
		dealed_count=0
		while self.status == 1:
			line=f.readline()
			if not line:
				break
			result = self.handle(line)
			print result
			if output: output.write(result + '\n')
			dealed_count+=1
			self.total_count+=1
			last_offset=f.tell()
			# record result
			if dealed_count%10 == 0:
				ftemp=open(tempfilename, 'w')
				ftemp.write(str(last_offset))
				ftemp.close()
				if output: output.flush()
		#
		ftemp=open(tempfilename, 'w')
		ftemp.write(str(last_offset))
		ftemp.close()
		if output: output.flush()
	
	def prepare_file(self, in_file, out_file=None):
		self.input_file=in_file
		self.output_file=out_file
	
	def run(self):
		self.status = 1
		ret = self.deal_file(self.input_file, self.output_file)
		self.status = 0
		return ret
	def stop(self):
		self.status = 0
	
	def get_status(self):
		return self.status
	def get_lasterror(self):
		return self.lasterror
	def get_totalcount(self):
		return self.total_count
	def get_filecount(self):
		#
		f=open(self.input_file)
		lines=f.readlines()
		infile_count=len(lines)
		f.close
		#
		outfile_count = -1
		if self.output_file:
			f=open(self.output_file)
			lines=f.readlines()
			outfile_count=len(lines)-1
			f.close
		#
		return (infile_count,outfile_count)
	
if __name__ == '__main__':
	poster = HandlerBase('23')
	poster.prepare_file('R:/input.txt', 'R:/output.csv')
	print 'start thread..'
	poster.start()
	print 'wait thread complete ..'
	poster.join()

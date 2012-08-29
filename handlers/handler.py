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
		self.output_header = 'status,echo\n'.decode('utf-8').encode('gbk')
	
	def handle(self, line):
		return ["1", line]
	
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
			output.write(self.output_header)
			output.flush()
		# deal
		dealed_count=0
		while True:
			line=f.readline()
			if not line:
				break
			result = self.handle(line)
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
		f=open(self.input_file)
		lines=f.readlines()
		infile_count=len(lines)
		f.close
		#
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

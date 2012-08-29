#!/usr/bin/env python
# encoding: UTF-8

import os,fnmatch
import web

from common.globalfunc import render,jsonize
import logging
logger = logging.getLogger()

import sys
sys.path.append('..')
from handlers.linkweight import GetLinkWeight as CHandler

BATCH_WEIGHT_DIR = 'D:/link_weight/'
urls = (
	'/?', 'index',
	'/files', 'files',
    '/query/(.*)', 'query',
	'/handle/(.*)', 'handle',
)

class index:
	def GET(self):
		return render.batchweight(filedir=BATCH_WEIGHT_DIR)

class files:
	@jsonize
	def GET(self):
		file_list = []
		for file_name in os.listdir(BATCH_WEIGHT_DIR):
			if fnmatch.fnmatch( file_name, '*.txt' ):
				file_list.append(file_name.decode('gbk').encode('utf-8'))
		return dict(files=file_list)

filestat = {}
class query:
	@jsonize
	def GET(self, filename=None):
		logger.debug("GET filename="+filename)
		print filestat
		handler = filestat.get(filename)
		status = 0
		ret = {}
		if handler is not None:
			status = handler.get_status()
			if status>0:
				count1=handler.get_totalcount()
				ret = dict(status=status,count1=count1)
			else:
				handler.join(0.01)
				(count1,count2)=handler.get_filecount()
				lasterror=handler.get_lasterror()
				ret = dict(status=status,count1=count1,count2=count2,lasterror=lasterror)
		return ret

class handle:
	@jsonize
	def POST(self, filename):
		out_file = filename[:-4]+"_out.csv"
		print "batchweight.POST(in="+BATCH_WEIGHT_DIR+filename+", out="+BATCH_WEIGHT_DIR+out_file+")"
		i = web.input()
		email = i.email
		passwd = i.passwd
		print "batchweight.POST(email="+email+", passwd="+passwd+")"
		handler = CHandler(email)
		handler.prepare_file(BATCH_WEIGHT_DIR+filename, BATCH_WEIGHT_DIR+out_file)
		if email and passwd:
			handler.login(email, passwd)
		handler.start()
		filestat[filename] = handler
		return dict(file=filename)

app = web.application(urls, locals(), autoreload=True)

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	app.run()

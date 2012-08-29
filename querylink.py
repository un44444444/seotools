#!/usr/bin/env python
# encoding: UTF-8

import os,fnmatch
import web

from common.globalfunc import render,jsonize
import logging
logger = logging.getLogger()

import sys
sys.path.append('..')
from handlers.queryexlink import QueryExternalLink as CHandler

EXTERNAL_LINK_DIR = 'D:/external_link/'
urls = (
	'/?', 'index',
	'/files', 'files',
    '/query/(.*)', 'query',
	'/handle/(.*)', 'handle',
)

class index:
	def GET(self):
		return render.queryexlink(filedir=EXTERNAL_LINK_DIR)

class files:
	@jsonize
	def GET(self):
		file_list = []
		for file_name in os.listdir(EXTERNAL_LINK_DIR):
			if fnmatch.fnmatch( file_name, '*.csv' ):
				if len(file_name)>7 and file_name[-8:-4]=='_out':
					continue
				file_list.append(file_name.decode('gbk').encode('utf-8'))
		return dict(files=file_list)

exlink_filestat = {}
class query:
	@jsonize
	def GET(self, filename):
		logger.debug("GET filename="+filename)
		print exlink_filestat
		handler = exlink_filestat.get(filename)
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
		print "queryexlink.POST(in="+EXTERNAL_LINK_DIR+filename+", out="+EXTERNAL_LINK_DIR+out_file+")"
		i = web.input()
		email = i.email
		passwd = i.passwd
		print "queryexlink.POST(email="+email+", passwd="+passwd+")"
		handler = CHandler(email)
		handler.prepare_file(EXTERNAL_LINK_DIR+filename, EXTERNAL_LINK_DIR+out_file)
		if email and passwd:
			handler.login(email, passwd)
		handler.start()
		exlink_filestat[filename] = handler
		return dict(file=filename)

app = web.application(urls, locals(), autoreload=True)

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	app.run()

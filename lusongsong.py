#!/usr/bin/env python
# encoding: UTF-8

import os,fnmatch
import web

from common.globalfunc import render,jsonize
import logging
logger = logging.getLogger()

from common.config import config
from handlers.lusongsong import OpenLusongsong as CHandler

urls = (
	'/?', 'index',
	'/files', 'files',
    '/query/(.*)', 'query',
	'/handle/(.*)', 'handle',
)

class index:
	def GET(self):
		return render.lusongsong(filedir=config.lusongsong.filedir)

class files:
	@jsonize
	def GET(self):
		file_list = []
		for file_name in os.listdir(config.lusongsong.filedir):
			if fnmatch.fnmatch( file_name, '*.txt' ):
				file_list.append(file_name.decode('gbk').encode('utf-8'))
		return dict(files=file_list)

filestat = {}
class query:
	@jsonize
	def GET(self, filename=None):
		logger.debug("%s.query::GET(filename=%s)" % (__name__, filename))
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
		logger.debug("%s.handle::POST(in=%s)" % (__name__, config.lusongsong.filedir+filename))
		handler = CHandler()
		handler.prepare_file(config.lusongsong.filedir+filename)
		handler.start()
		filestat[filename] = handler
		return dict(file=filename)

app = web.application(urls, locals(), autoreload=True)

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	app.run()

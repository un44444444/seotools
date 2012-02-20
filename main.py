#!/usr/bin/env python
# encoding: UTF-8

__version__ = '0.1'

import sys, os
try:
	import json
except ImportError:
	import simplejson as json
import logging
import fnmatch

import web
from web.contrib.template import render_mako

sys.path.append(os.sep.join((os.getcwd(),'lib')))
#print os.sep.join((os.getcwd(),'lib'))
#sys.path(os.sep.join((os.getcwd(),'lib')))
import onering

from filemgr import FileMgr
from website import WebsitesMgr

FILE_DIR = 'D:/seo_articles/'
BATCH_WEIGHT_DIR = 'D:/link_weight/'

urls = (
	'/init', 'init',
	'/', 'index',
	'/about', 'about',
	'/static/(.*)', 'static',
	'/filemgr', 'filemgr',
	'/data/test', 'data_test',
	'/autosend/(.*)', 'autosend',
	'/data/send/(.*)', 'data_send',
	'/data/seccode/(.*)', 'data_seccode',
	'/data/secqaa/(.*)', 'data_secqaa',
	'/filelist', 'filelist',
	'/data/filelist', 'data_filelist',
	'/batchweight', 'batchweight',
	'/batchweight/(.*)', 'batchweight',
	'/data/batchweight', 'data_batchweight',
	'/file/(.*)', 'fileshow',
	'/data/file/(.*)', 'data_file',
	'/warning/(.*)', 'warning',
)

render = render_mako(
	directories=['templates'],
	input_encoding='utf8',
	output_encoding='utf8',
)

def jsonize(func):
	def _(*a, **kw):
		ret = func(*a, **kw)
		web.header('Content-Type', 'application/json')
		return json.dumps(ret)
	return _

class init:
	@jsonize
	def GET(self):
		url = ('/' + startup_demo) if startup_demo else '/'
		return dict(width=640, height=480, title="SEO Tools", url=url,
					appname="SEO Tools", icon="/static/favicon.ico",
				)

class index:
	def GET(self):
		return render.index()

class about:
	def GET(self):
		return render.about()

class filemgr:
	def GET(self):
		return render.filemgr()

class autosend:
	def GET(self, filename):
		#websites = ['bbs.hangzhou.com.cn',]
		websites = ['bbs.hef'+'ei.cc','bbs.vo'+'c.com.cn','bbs.66'+'163.com','bbs.hangzho'+'u.com.cn']
		return render.autosend(filename=filename, websites=websites)

class data_seccode:
	@jsonize
	def GET(self, website):
		site = WebsitesMgr.getInst(website)
		filename = site.getSecimage()
		return dict(name=filename)

class data_secqaa:
	@jsonize
	def GET(self, website):
		site = WebsitesMgr.getInst(website)
		(q,a) = site.getSecqaa()
		return dict(q=q, a=a)

class data_send:
	@jsonize
	def POST(self, website):
		print "data_send.POST"
		i = web.input()
		title = i.title
		content = i.content
		seccode = str(i.seccode)
		secqaa = ''
		if hasattr(i,'secqaa'):
			secqaa = i.secqaa
		site = WebsitesMgr.getInst(website)
		url = site.postArctle(title, content, seccode, secqaa)
		return dict(name=url)

class filelist:
	def GET(self):
		return render.filelist()

class data_filelist:
	@jsonize
	def GET(self):
		file_list = []
		for file_name in os.listdir(FILE_DIR):
			if fnmatch.fnmatch( file_name, '*.txt' ):
				file_list.append(file_name.decode('gbk').encode('utf-8'))
		return dict(files=file_list)

filestat = {}
class batchweight:
	def GET(self, file=None):
		if file is None:
			return render.batchweight(filedir=BATCH_WEIGHT_DIR)
		print "GET file="+file
		print filestat
		handler = filestat.get(file)
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
		web.header('Content-Type', 'application/json')
		return json.dumps(ret)
	@jsonize
	def POST(self, file):
		out_file = file[:-4]+"_out.csv"
		print "batchweight.POST(in="+BATCH_WEIGHT_DIR+file+", out="+BATCH_WEIGHT_DIR+out_file+")"
		i = web.input()
		email = i.email
		passwd = i.passwd
		print "batchweight.POST(email="+email+", passwd="+passwd+")"
		import linkweight
		handler = linkweight.GetLinkWeight(email)
		handler.prepare_file(BATCH_WEIGHT_DIR+file, BATCH_WEIGHT_DIR+out_file)
		if email and passwd:
			handler.login(email, passwd)
		handler.start()
		filestat[file] = handler
		return dict(file=file)

class data_batchweight:
	@jsonize
	def GET(self):
		file_list = []
		for file_name in os.listdir(BATCH_WEIGHT_DIR):
			if fnmatch.fnmatch( file_name, '*.txt' ):
				file_list.append(file_name.decode('gbk').encode('utf-8'))
		return dict(files=file_list)

class fileshow:
	def GET(self, filename):
		return render.fileshow(filename=filename)

class data_file:
	@jsonize
	def GET(self, filename):
		#
		title = filename.replace('.txt','')
		try:
			title = title.decode('gbk').encode('utf-8')
		except:
			pass
		#
		content = open('%s%s' % (FILE_DIR,filename), 'r').read()
		try:
			content = content.decode('gbk').encode('utf-8')
		except:
			pass
		#
		return dict(title=title, content=content)

class warning:
	def GET(self, msg=None):
		return render.warning(msg=msg)

class data_test:
	@jsonize
	def GET(self):
		#return dict(data="test data.")
		filemgr = FileMgr()
		catelogs = filemgr.get_catelogs()
		return catelogs

class static:
	def GET(self, filename):
		#print filename
		content = open('static/%s' % filename, 'rb').read()
		content_types = {
			'.js': 'text/javascript',
			'.css': 'text/css',
			'.ico': 'image/x-icon',
		}
		ext = os.path.splitext(filename)[1]
		content_type = content_types.get(ext, 'application/octet-stream')
		web.header('Content-Type', content_type)
		web.header('Content-Length', len(content))
		return content

if '-v' in sys.argv:
	logging.basicConfig(level=logging.DEBUG)
else:
	logging.basicConfig()

if '--demo' in sys.argv:
	startup_demo = sys.argv[sys.argv.index('--demo')+1]
else:
	startup_demo = None

app = web.application(urls, globals(), autoreload=True)

if __name__ == '__main__':
	onering.register_wsgi_app("demo", app.wsgifunc())
	onering.loop("demo")

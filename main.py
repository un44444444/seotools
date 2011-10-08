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
from discuz_auth import Discuz,DiscuzSingleton

urls = (
	'/init', 'init',
	'/', 'index',
	'/about', 'about',
	'/static/(.*)', 'static',
	'/filemgr', 'filemgr',
	'/data/test', 'data_test',
	'/autosend', 'autosend',
	'/data/send', 'data_send',
	'/filelist', 'filelist',
	'/data/filelist', 'data_filelist',
	'/data/file/(.*)', 'data_file',
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
	def GET(self):
		return render.autosend()

class data_send:
	def __init__(self):
		param = {
			'url':'http://localhost/discuz/',
			'image_base':'static/secimage/',
		}
		self.discuz = DiscuzSingleton.getInst(param)
		self.fid = 2
	
	@jsonize
	def GET(self):
		self.discuz.login('un44444444', '44444444')
		filename = self.discuz.getSeccode(self.fid)
		return dict(name=filename)
	
	@jsonize
	def POST(self):
		i = web.input()
		seccode = str(i.seccode)
		title = u'测试1文章'.encode('gbk','ignore');
		content = u'测试2内容!测试3内容!'.encode('gbk','ignore')
		url = self.discuz.post(self.fid, title, content, seccode)
		url = url.decode('gbk').encode('utf-8')
		return dict(name=url)

class filelist:
	def GET(self):
		return render.filelist()

class data_filelist:
	@jsonize
	def GET(self):
		path = 'R:/'
		file_list = []
		for file_name in os.listdir(path):
			if fnmatch.fnmatch( file_name, '*.txt' ):
				file_list.append(file_name.decode('gbk').encode('utf-8'))
		return dict(files=file_list)

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
		content = open('R:/%s' % filename, 'r').read()
		try:
			content = content.decode('gbk').encode('utf-8')
		except:
			pass
		#
		return dict(title=title, content=content)

class data_test:
	@jsonize
	def GET(self):
		#return dict(data="test data.")
		filemgr = FileMgr()
		catelogs = filemgr.get_catelogs()
		return catelogs

class static:
	def GET(self, filename):
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

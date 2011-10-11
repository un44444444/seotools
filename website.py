#!/usr/bin/env python
# encoding: UTF-8

import string
from discuz_x2 import Discuz as discuz_x2
from discuz_600 import Discuz as discuz_600

websites = {
	'localhost':{
		'model': 'discuz_x2',
		'url': 'http://localhost/discuz/',
		'image_base':'static/secimage/',
		'encoding':'gbk',
		'username': 'un44444444',
		'password': '44444444',
		'fid': 2,
	},
	'bbs.55bbs.com':{
		'model': 'discuz_600',
		'url': 'http://bbs.55bbs.com/',
		'image_base':'static/secimage/55bbs_',
		'encoding':'gbk',
		'username': 'un44444444',
		'password': '44444444',
		'fid': 2,
	},
}

class Website:
	def __init__(self, name):
		conf = websites[name]
		self.fid = conf['fid']
		constructor = globals()[conf['model']]
		self.discuz = constructor(conf)
		self.discuz.login(conf['username'], conf['password'])
	
	def getSecimage(self):
		return self.discuz.getSeccode(self.fid)
	
	def postArctle(self, title, content, seccode):
#		title = u'测试1文章'.encode('gbk','ignore');
#		content = u'测试2内容!测试3内容!'.encode('gbk','ignore')
		title = title.encode('gbk');
		content = content.encode('gbk');
		url = self.discuz.post(self.fid, title, content, seccode)
		url = url.decode('gbk').encode('utf-8')
		return url

class WebsitesMgr:
	def __init__(self):
		"disable the __init__ method"
	
	__inst = {} # make it so-called private
	
	@staticmethod
	def getInst(name):
		if not WebsitesMgr.__inst.has_key(name):
			WebsitesMgr.__inst[name] = Website(name)
		return WebsitesMgr.__inst[name]

if __name__ == '__main__':
	pass

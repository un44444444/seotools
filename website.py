#!/usr/bin/env python
# encoding: UTF-8

import discuz_auth

websites = {
	'localhost':{
		'model': 'discuz_auth.Discuz',
		'url': 'http://localhost/discuz/',
		'image_base':'static/secimage/',
		'encoding':'gbk',
		'username': 'un44444444',
		'password': '44444444',
		'fid': 2,
	},
	'bbs.55bbs.com':{
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
		self.discuz = discuz_auth.Discuz(conf)
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

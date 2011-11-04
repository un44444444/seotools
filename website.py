#!/usr/bin/env python
# encoding: UTF-8

import string
from discuz_x2 import Discuz as discuz_x2
from discuz_600 import Discuz as discuz_600
from discuz_610 import Discuz as discuz_610
from discuz_voc import Discuz as discuz_voc

websites = {
	'localhost':{
		'model': 'discuz_x2',
		'url': 'http://localhost/discuz/',
		'image_base':'static/secimage/',
		'encoding':'gbk',
		'username': 'un44444444',
		'password': '44444444',
		'fid': 2,
		'need_secimg': True,
		'need_secqaa': False,
	},
	'bbs.55bbs.com':{
		'model': 'discuz_600',
		'url': 'http://bbs.55bbs.com/',
		#'url': 'http://localhost/discuz_600/',
		'image_base':'static/secimage/bbs.55bbs.com_',
		'encoding':'gbk',
		'username': 'un44444444',
		'password': 'un44444444',
		'fid': 30,
		#'fid': 2,
		'need_secimg': True,
		'need_secqaa': False,
	},
	'bbs.hefei.cc':{
		'model': 'discuz_610',
		'url': 'http://bbs.hefei.cc/',
		'image_base':'static/secimage/bbs.hefei.cc_',
		'encoding':'gbk',
		'username': 'un44444444',
		'password': '44444444',
		'fid': 34,
		'need_secimg': True,
		'need_secqaa': True,
	},
	'bbs.voc.com.cn':{
		'model': 'discuz_voc',
		'url': 'http://bbs.voc.com.cn/',
		'image_base':'static/secimage/bbs.voc.com.cn_',
		'encoding':'gbk',
		'username': 'un44444444',
		'password': 'un44444444',
		'fid': 52,
		'need_secimg': False,
		'need_secqaa': False,
	},
	'bbs.66163.com':{
		'model': 'discuz_x2',
		'url': 'http://bbs.66163.com/',
		'image_base':'static/secimage/bbs.66163.com_',
		'encoding':'gbk',
		'username': 'un44444444',
		'password': '44444444',
		'fid': 27,
		'need_secimg': True,
		'need_secqaa': False,
	},
	'bbs.hangzhou.com.cn':{
		'model': 'discuz_x2',
		'url': 'http://bbs.hangzhou.com.cn/',
		'image_base':'static/secimage/bbs.hangzhou.com.cn_',
		'encoding':'gbk',
		'username': 'un44444444',
		'password': '44444444',
		'fid': 201,
		'need_secimg': False,
		'need_secqaa': False,
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
		if not self.discuz.conf['need_secimg']:
			return ''
		return self.discuz.getSeccode(self.fid)
	
	def getSecqaa(self):
		if not self.discuz.conf['need_secqaa']:
			return ('','')
		if hasattr(self.discuz,'getSecqaa'):
			return self.discuz.getSecqaa(self.fid)
		else:
			return ('','')
	
	def postArctle(self, title, content, seccode, secqaa=''):
#		title = u'测试1文章'.encode('gbk','ignore');
#		content = u'测试2内容!测试3内容!'.encode('gbk','ignore')
		title = title.encode('gbk');
		content = content.encode('gbk');
		secqaa = secqaa.encode('gbk');
		url = self.discuz.post(self.fid, title, content, seccode, secqaa)
		url = url.decode('gbk').encode('utf-8')
		return url

class WebsitesMgr:
	def __init__(self):
		"disable the __init__ method"
	
	__inst = {} # make it so-called private
	
	@staticmethod
	def getInst(name):
		if WebsitesMgr.__inst.has_key(name):
			return WebsitesMgr.__inst[name]
		website = Website(name)
		WebsitesMgr.__inst[name] = website
		return website

if __name__ == '__main__':
	pass

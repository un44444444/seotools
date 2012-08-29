#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: discuz_600.py

import string
import re
import random
from discuz import DiscuzBase

class Discuz(DiscuzBase):
	def __init__(self, param):
		self.conf = {
			'url':'http://localhost/discuz_600/',
			'encoding':'gbk',
			'image_base':'R:/',
			'action_login':string.Template('logging.php?action=login'),
			'action_login_referer':'',
			'action_preparepost':string.Template('post.php?action=newthread&fid=$fid&extra=20'),
			'action_post':string.Template('post.php?action=newthread&fid=$fid&inajax=1&extra=20&topicsubmit=yes'),
			'action_seccode':string.Template('seccode.php?update=0.${randstr}'),
		}
		self.conf.update(param)
		#
		DiscuzBase.__init__(self)
		self.url = self.conf['url']
		self.encoding = self.conf['encoding']
		self.image_base = self.conf['image_base']
		self.formhash = ''

	def login(self,username,password):
		logindata=(('loginfield','username'), ('username',username), ('password',password), ('loginsubmit','true'))
		self.action_login = self.url + self.conf['action_login'].substitute()
		content = self.request_post(self.action_login, logindata, self.conf['action_login_referer'])
		error_message = self.get_error_message(content)
		return error_message

	def _preparePost(self,fid):
		self.action_preparepost = self.url + self.conf['action_preparepost'].substitute(fid=fid)
		content = self.request_get(self.action_preparepost)
		#print content.decode()
		error_message = self.get_error_message(content)
		if error_message:
			print error_message
			return error_message
		#
		try:
			str_re='<input\s*type="hidden"\s*name="formhash"\s*id="formhash"\s*value="(.*?)"\s*\/>'
			reObj=re.compile(str_re)
			allMatch=reObj.findall(content)
			self.formhash=allMatch[0]
			#print formhash
		except Exception,e:
			print e
			print content
			exit(1)
		#print content
		return self.action_preparepost

	def getSeccode(self,fid):
		#
		self._preparePost(fid)
		#
		rand1 = random.randint(10000000,99999999)
		rand2 = random.randint(10000000,99999999)
		randstr = '%d%d'%(rand1,rand2)
		action_seccode = self.url + self.conf['action_seccode'].substitute(randstr=randstr)
		content = self.request_get(action_seccode, self.action_preparepost)
		#print content
		file_name = 'secimage_'+randstr+'.png'
		f = open(self.image_base + file_name,"wb")
		f.write(content)
		f.close()
		return file_name

	def post(self,fid,title,contents, seccode='',secqaa=''):
		""""post content"""
		if not self.formhash:
			self._preparePost(fid)
		postdata=[("formhash",self.formhash),("isblog",""),("frombbs","1"),("subject",title),("iconid","0"),("message",contents),("tag",""),("wysiwyg","1")]
		self.formhash = ''
		if seccode:
			postdata.append(("seccodeverify",seccode))
		if secqaa:
			postdata.append(("secanswer",secqaa))
		#print postdata
		action_post = self.url + self.conf['action_post'].substitute(fid=fid)
		content = self.post_then_fetch_url(action_post, tuple(postdata), self.action_preparepost)
		#
		if len(content) < 128:
			return content
		#
		str_re='<br\s\/><br\s\/><a\shref="(.*?)">\['
		reObj=re.compile(str_re)
		allMatch=reObj.findall(content)
		if len(allMatch) == 1:
			return self.url + allMatch[0]
		#
		error_msg = self.get_error_message(content)
		return error_msg


if __name__ == "__main__":
#	try:
		param = {
			'url':'http://localhost/discuz_600/',
			'username':'un44444444',
		}
		fid = 30
		discuz = Discuz(param)
		discuz.login(param['username'], 'un44444444')
		#exit()
		#
		local_file = discuz.getSeccode(fid)
		print local_file
		seccode = input("Input seccode from image:")
		#
		title = u'测试文章'.encode('gbk','ignore');
		content = u'测试内容!测试内容!'.encode('gbk','ignore')
		post_url = discuz.post(fid, title, content, seccode)
		print post_url
#	except Exception,e:
#		print 'Error'
#		print e

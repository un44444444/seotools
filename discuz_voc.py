#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: discuz_voc.py

import string
import re
import hashlib
from discuz import DiscuzBase

class Discuz(DiscuzBase):
	def __init__(self, param):
		self.conf = {
			'url':'http://localhost/discuz_610/',
			'encoding':'gbk',
			'image_base':'R:/',
			'action_login':string.Template('logging.php?action=login'),
			'action_login_referer':'',
			'action_preparepost':string.Template('post.php?action=newthread&fid=$fid&extra=page%3D1'),
			'action_post':string.Template('post.php?action=newthread&fid=$fid&extra=page%3D1&topicsubmit=yes'),
			'action_secqaa':string.Template('ajax.php?action=updatesecqaa&inajax=1'),
			'action_seccode':string.Template('ajax.php?action=updateseccode&inajax=1'),
		}
		self.conf.update(param)
		#
		DiscuzBase.__init__(self)
		self.url = self.conf['url']
		self.encoding = self.conf['encoding']
		self.image_base = self.conf['image_base']
		self.formhash = ''
		self.username = ''
		self.psw_md5 = ''

	def login(self,username,password):
		self.username = username
		self.psw_md5 = hashlib.md5(password).hexdigest()
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
			str_re='<input\s*type="hidden"\s*name="formhash"\s*id="formhash"\s*value="(.*?)"\s*\/?>'
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

	def post(self,fid,title,contents, seccode='',secqaa=''):
		""""post content"""
		if not self.formhash:
			self._preparePost(fid)
		postdata=[("formhash",self.formhash),("frombbs","1")]
		self.formhash = ''
		if seccode:
			postdata.append(("seccodeverify",seccode))
		if secqaa:
			postdata.append(("secanswer",secqaa))
		postdata.extend([("typeid","2"),("subject",title),("iconid","0"),("username",self.username),("password",self.psw_md5),("message",contents),("tag",""),("readperm","0"),("iconid","0"),("wysiwyg","1")])
		#print postdata
		action_post = self.url + self.conf['action_post'].substitute(fid=fid)
		content = self.post_then_fetch_url(action_post,tuple(postdata),self.action_preparepost)
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
			'url':'http://localhost/discuz_voc/',
			'username':'un44444444',
		}
		fid = 52
		discuz = Discuz(param)
		discuz.login(param['username'], 'un44444444')
		#
		title = u'云计算'.encode('gbk','ignore');
		content = u'中国一留学生去美国打工的当过报童，不带计算器，习惯动作抬头望天时心算找零。顾客大为惊讶，纷纷掏出计算器验证，皆无误，也抬头望天，惊恐问：“云计算？'.encode('gbk','ignore')
		post_url = discuz.post(fid, title, content)
		print post_url
#	except Exception,e:
#		print 'Error'
#		print e

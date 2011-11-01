#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: discuz.py

import string
import urllib2
import re,time
from discuz import Discuz

class Discuz610(Discuz):
	def __init__(self, param):
		Discuz.__init__(self)
		#
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
		try:
			self._getResultInfo(content)
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

	def getSecqaa(self,fid):
		#
		if not self.formhash:
			self._preparePost(fid)
		#
		action_secqaa = self.url + self.conf['action_secqaa'].substitute()
		content = self.request_get(action_secqaa)
		#print content
		try:
			self._getResultInfo(content)
			str_re='<root><!\[CDATA\[(.*?)\]\]></root>'
			reObj=re.compile(str_re)
			allMatch=reObj.findall(content)
			qaa=allMatch[0]
			try:
				qaa = qaa.decode('gbk').encode('utf-8')
			except:
				pass
			#print img_src
		except Exception,e:
			print e
			print content
			exit(1)
		#
		if '<' == qaa[0]:
			try:
				str_re='<img\s*src="(.*?)"\s*\/?>(.*)'
				reObj=re.compile(str_re)
				allMatch=reObj.findall(qaa)
				(img_src,a)=allMatch[0]
			except Exception,e:
				print e
				print content
				exit(1)
			#download imgage to local
			remote_img = self.url + img_src
			print remote_img
			req = urllib2.Request(remote_img)
			req.add_header('Referer', self.action_preparepost)
			data = urllib2.urlopen(req).read()
			file_name = 'checkimage'+str(time.time())+'.png'
			f = open(self.image_base + file_name,"wb")
			f.write(data)
			f.close()
			return (file_name, a)
		else:
			try:
				a=''
				str_re='.*答案:(.*?)$'
				reObj=re.compile(str_re)
				allMatch=reObj.findall(qaa)
				a=allMatch[0]
			except:
				pass
			return (qaa, a)

	def getSeccode(self,fid):
		#
		if not self.formhash:
			self._preparePost(fid)
		#
		action_seccode = self.url + self.conf['action_seccode'].substitute()
		content = self.request_get(action_seccode)
		#print content
		try:
			self._getResultInfo(content)
			str_re='<img\s*.*\s*src="(.*?)"\s*.*\/>'
			reObj=re.compile(str_re)
			allMatch=reObj.findall(content)
			img_src=allMatch[0]
			#print img_src
		except Exception,e:
			print e
			print content
			exit(1)
		#
		str_re='update=([0-9]*)'
		reObj=re.compile(str_re)
		allMatch=reObj.findall(img_src)
		img_update=allMatch[0]
		#download imgage to local
		remote_img = self.url + img_src
		print remote_img
		req = urllib2.Request(remote_img)
		req.add_header('Referer', self.action_preparepost)
		data = urllib2.urlopen(req).read()
		file_name = 'secimage_'+img_update+'.png'
		f = open(self.image_base + file_name,"wb")
		f.write(data)
		f.close()
		return file_name

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
		postdata.extend([("typeid","2"),("subject",title),("iconid","0"),("message",contents),("tag",""),("readperm","0"),("iconid","0"),("wysiwyg","1")])
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
			'url':'http://bbs.voc.com.cn/',
		}
		fid = 52
		discuz = Discuz(param)
		discuz.login('un44444444', 'un44444444')
		#exit()
		#
#		(q,a) = discuz.getSecqaa(fid)
#		print q
#		print a
#		local_file = discuz.getSeccode(fid)
#		print local_file
		seccode = input("Input seccode from image:")
		#
		title = u'云计算'.encode('gbk','ignore');
		content = u'中国一留学生去美国打工的当过报童，不带计算器，习惯动作抬头望天时心算找零。顾客大为惊讶，纷纷掏出计算器验证，皆无误，也抬头望天，惊恐问：“云计算？'.encode('gbk','ignore')
		post_url = discuz.post(fid, title, content, seccode)
		print post_url
#	except Exception,e:
#		print 'Error'
#		print e

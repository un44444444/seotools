#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: discuz_x2.py

import string
import re
from discuz import DiscuzBase

class Discuz(DiscuzBase):
	def __init__(self, param):
		self.conf = {
			'url':'http://localhost/discuz/',
			'encoding':'gbk',
			'image_base':'R:/',
			'action_login':string.Template('member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LIQ5i'),
			'action_login_referer':'',
			'action_preparepost':string.Template('forum.php?mod=post&action=newthread&fid=$fid'),
			'action_post':string.Template('forum.php?mod=post&action=newthread&extra=&topicsubmit=yes&fid=$fid'),
			'action_seccode':string.Template('misc.php?mod=seccode&action=update&idhash=${sechash}&inajax=1&ajaxtarget=seccode_${sechash}'),
		}
		self.conf.update(param)
		#
		DiscuzBase.__init__(self)
		self.url = self.conf['url']
		self.encoding = self.conf['encoding']
		self.image_base = self.conf['image_base']
		self.formhash = ''
		self.posttime = ''
		self.sechash = ''

	def login(self,username,password):
		logindata=(('username',username), ('password',password))
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
			str_re='<input\s*type="hidden"\s*name="posttime"\s*id="posttime"\s*value="(.*?)"\s*\/>'
			reObj=re.compile(str_re)
			allMatch=reObj.findall(content)
			self.posttime=allMatch[0]
			#print posttime
			str_re='onclick="updateseccode\(\'(.*?)\'\);doane\(event\);"'
			reObj=re.compile(str_re)
			allMatch=reObj.findall(content)
			self.sechash=allMatch[0]
			#print sechash
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
		action_seccode = self.url + self.conf['action_seccode'].substitute(sechash=self.sechash)
		content = self.request_get(action_seccode)
		#print content
		error_message = self.get_error_message(content)
		if error_message:
			print error_message
			return error_message
		#
		try:
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
		data = self.request_get_simple(remote_img, self.action_preparepost)
		file_name = 'secimage_'+self.sechash+'_'+img_update+'.png'
		f = open(self.image_base + file_name,"wb")
		f.write(data)
		f.close()
		return file_name

	def post(self,fid,title,contents, seccode='',secqaa=''):
		""""post content"""
		if not self.formhash:
			self._preparePost(fid)
		postdata=[("formhash",self.formhash),("posttime",self.posttime),("wysiwyg","1"),("subject",title),("message",contents),("sechash",self.sechash)]
		self.formhash = ''
		if seccode:
			postdata.append(("seccodeverify",seccode))
		if secqaa:
			postdata.append(("secanswer",secqaa))
		#print postdata
		action_post = self.url + self.conf['action_post'].substitute(fid=fid)
		content = self.post_then_fetch_url(action_post,tuple(postdata),self.action_preparepost)
		if len(content) > 128:
			error_msg = self.get_error_message(content)
			return error_msg
		#f=open('test.html',"w")
		#f.write(content)
		#f.close()
		return content


if __name__ == "__main__":
#	try:
		param = {
			'url':'http://localhost/discuz/',
			'username':'un44444444',
		}
		fid = 2
		discuz = Discuz(param)
		print "end"
#		response = urllib2.urlopen('http://localhost/discuz/')
#		info = response.info()
#		print info
#		print info.headers
#		server = info.getheader('Server', '')
#		print server
#		exit()
#		discuz.login(param['username'], '44444444')
#		#
#		local_file = discuz.getSeccode(fid)
#		print local_file
#		seccode = input("Input seccode from image:")
#		#
#		title = u'测试文章'.encode('gbk','ignore');
#		content = u'测试内容!测试内容!'.encode('gbk','ignore')
#		post_url = discuz.post(fid, title, content, seccode)
#		print post_url
#	except Exception,e:
#		print 'Error'
#		print e

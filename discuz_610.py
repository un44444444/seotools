#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: discuz.py

import string
import urllib,urllib2
import re,time
import opener

class Discuz:
	def __init__(self, param):
		#self.opener = opener.getOpenerWithCookie()
		opener.installOpenerWithCookie()
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
		req=urllib2.Request(self.action_login,urllib.urlencode(logindata))
		if self.conf['action_login_referer']:
			req.add_header('Referer', self.conf['action_login_referer'])
		content = ""
		err_count = 0
		flage = True
		while flage:
			try:
				u=urllib2.urlopen(req)
				#u=self.opener.open(req)
				content=u.read()
				flage=False
				self._getResultInfo(content)
			except urllib2.HTTPError, e:
				if err_count > 10:
					exit(1)
				err_count += 1
				print e
				flage = True
				if e.getcode()== 403:
					print "Wait for 5 minutes..."
					time.sleep(5 * 60)

		#print content
		return content

	def _getResultInfo(self,content):
		p = re.compile('<div\s*id="messagetext"\s*class="alert_error"\s*>\s*<p>(.*?)\s*<script\s*')
		m = p.findall(content)
		if len(m) > 0:
			for i in m:
				print  i.replace('</p>','').decode(self.encoding,'ignore')
			return m[0].replace('</p>','')
		else:
			return ''

	def _preparePost(self,fid):
		self.action_preparepost = self.url + self.conf['action_preparepost'].substitute(fid=fid)
		request=urllib2.Request(self.action_preparepost)
		content = ""
		err_count = 0
		flage = True
		while flage:
			try:
				page=urllib2.urlopen(request)
				#page=self.opener.open(request)
				content=page.read()

				flage=False
			except urllib2.HTTPError, e:
				if err_count > 10:
					exit(1)
				err_count += 1
				print e
				flage = True
				if e.getcode() == 403:
					print "Wait for 5 minutes..."
					time.sleep(5 * 60)
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
		request=urllib2.Request(action_secqaa)
		content = ""
		err_count = 0
		flage = True
		while flage:
			try:
				page=urllib2.urlopen(request)
				#page=self.opener.open(request)
				content=page.read()

				flage=False
			except urllib2.HTTPError, e:
				if err_count > 10:
					exit(1)
				err_count += 1
				print e
				flage = True
				if e.getcode() == 403:
					print "Wait for 5 minutes..."
					time.sleep(5 * 60)
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
		request=urllib2.Request(action_seccode)
		content = ""
		err_count = 0
		flage = True
		while flage:
			try:
				page=urllib2.urlopen(request)
				#page=self.opener.open(request)
				content=page.read()

				flage=False
			except urllib2.HTTPError, e:
				if err_count > 10:
					exit(1)
				err_count += 1
				print e
				flage = True
				if e.getcode() == 403:
					print "Wait for 5 minutes..."
					time.sleep(5 * 60)
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
		if seccode:
			postdata.append(("seccodeverify",seccode))
		if secqaa:
			postdata.append(("secanswer",secqaa))
		postdata.extend([("typeid","2"),("subject",title),("iconid","0"),("message",contents),("tag",""),("readperm","0"),("iconid","0"),("wysiwyg","1")])
		params=urllib.urlencode(tuple(postdata),self.encoding)
		#print params
		self.formhash = ''
		action_post = self.url + self.conf['action_post'].substitute(fid=fid)
		request=urllib2.Request(action_post,params)
		request.add_header('Referer', self.action_preparepost)
		content = ""
		err_count = 0
		flage=True
		while flage:
			try:
				response=urllib2.urlopen(request)
				#
				status_code=response.getcode()
				print status_code
				if status_code==301 or status_code==302:
					http_message=response.info()
					print http_message
					content=http_message.getheader('location', 'can not find location')
					return content
				#
				url=response.geturl()
				print url
				if url != action_post:
					return url
				#
				content=response.read()
				str_re='<br\s\/><br\s\/><a\shref="(.*?)">\['
				reObj=re.compile(str_re)
				allMatch=reObj.findall(content)
				if len(allMatch) == 1:
					return self.url + allMatch[0]
				flage=False
			except urllib2.HTTPError, e:
				if err_count > 10:
					exit(1)
				err_count += 1
				print e
				flage = True
				if e.getcode() == 403:
					print "Wait for 5 minutes..."
					time.sleep(5 * 60)
		content = self._getResultInfo(content)
		#f=open('test.html',"w")
		#f.write(content)
		#f.close()
		return content


if __name__ == "__main__":
#	try:
		param = {
			'url':'http://bbs.hefei.cc/',
		}
		fid = 34
		discuz = Discuz(param)
		discuz.login('un44444444', '44444444')
		#exit()
		#
		(q,a) = discuz.getSecqaa(fid)
		print q
		print a
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

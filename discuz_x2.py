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
		self.url = self.conf['url']
		self.encoding = self.conf['encoding']
		self.image_base = self.conf['image_base']
		#print "Discuz.__init__"
		self.formhash = ''
		self.posttime = ''
		self.sechash = ''

	def login(self,username,password):
		logindata=(('username',username), ('password',password))
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
		request=urllib2.Request(action_seccode,urllib.urlencode(''))
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
		file_name = 'secimage_'+self.sechash+'_'+img_update+'.png'
		f = open(self.image_base + file_name,"wb")
		f.write(data)
		f.close()
		return file_name

	def post(self,fid,title,contents, seccode=''):
		""""post content"""
		if not self.formhash:
			self._preparePost(fid)
		postdata=(("formhash",self.formhash),("posttime",self.posttime),("wysiwyg","1"),("subject",title),("message",contents),("sechash",self.sechash),("seccodeverify",seccode))
		params=urllib.urlencode(postdata,self.encoding)
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
				if status_code == 301:
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
				print 'len(content):'+str(len(content))
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
			'url':'http://localhost/discuz/',
		}
		fid = 2
		discuz = Discuz(param)
#		response = urllib2.urlopen('http://localhost/discuz/')
#		info = response.info()
#		print info
#		print info.headers
#		server = info.getheader('Server', '')
#		print server
#		exit()
		discuz.login('un44444444', '44444444')
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

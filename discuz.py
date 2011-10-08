#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: discuz.py

import urllib,urllib2
import re,time
import opener

class Discuz:
	def __init__(self, param):
		#self.opener = opener.getOpenerWithCookie()
		opener.installOpenerWithCookie()
		#
		conf = {
			'url':'http://localhost/discuz/',
			'action_login':'member.php?mod=logging&action=login&loginsubmit=yes&handlekey=login&loginhash=LIQ5i',
			'action_post':'forum.php?mod=post&action=newthread',
			'encoding':'gbk',
		}
		conf.update(param)
		self.url = conf['url']
		self.action_login = self.url + conf['action_login']
		self.action_post = self.url + conf['action_post']
		self.encoding = conf['encoding']

	def login(self,username,password):
		logindata=(('username',username), ('password',password))
		req=urllib2.Request(self.action_login,urllib.urlencode(logindata))
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

	def post(self,fid,title,contents):
		action=self.action_post+'&fid='+str(fid)
		request=urllib2.Request(action,urllib.urlencode(''))
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
			formhash=allMatch[0]
			#print formhash
			str_re='<input\s*type="hidden"\s*name="posttime"\s*id="posttime"\s*value="(.*?)"\s*\/>'
			reObj=re.compile(str_re)
			allMatch=reObj.findall(content)
			posttime=allMatch[0]
			#print posttime
		except Exception,e:
			print e
			print content
			exit(1)
		#print content
		postdata=(("formhash",formhash),("posttime",posttime),("wysiwyg","1"),("subject",title),("message",contents),("save",""),("usesig","1"),("allownoticeauthor","1")) #,("typeid","28")
		params=urllib.urlencode(postdata,self.encoding)
		#print params
		action='forum.php?mod=post&action=newthread&fid='+str(fid)+'&extra=&topicsubmit=yes'
		request=urllib2.Request(self.url+action,params)
		content = ""
		err_count = 0
		flage=True
		while flage:
			try:
				page=urllib2.urlopen(request)
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
		self._getResultInfo(content)
		#f=open('test.html',"w")
		#f.write(content)
		#f.close()


if __name__ == "__main__":
#	try:
		param = {
			'url':'http://localhost/discuz/',
		}
		discuz = Discuz(param)
		discuz.login('un44444444', '44444444')
		title = u'测试文章'.encode('gbk','ignore');
		content = u'测试内容!测试内容!'.encode('gbk','ignore')
		discuz.post(2, title, content)
#	except Exception,e:
#		print 'Error'
#		print e

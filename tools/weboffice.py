#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: discuz_610.py

import string
import re,time
import base64

import sys
sys.path.append('..')
from common.http import HttpClient

class WebOffice(HttpClient):
	def __init__(self, param={}):
		self.conf = {
			'url':'http://zthf'+'tech.eic'+'p.net:180/',
			'encoding':'utf-8',
			'image_base':'R:/',
			'action_login':string.Template('portal/workflow/login.wf'),
			'action_login_referer':'portal/index_blue.jsp',
			'action_msglist':string.Template('portal/workflow/login.wf?sid=$sid&cmd=Navigation_Frame_Main&systemId=21'),
			'action_msglist_referer':string.Template('portal/workflow/login.wf?sid=$sid&cmd=Navigation_Frame_Top&systemId=21'),
			'action_msglist2':string.Template('portal/workflow/login.wf?sid=$sid&cmd=Portal_Execute_MessageWorkFlowTransaction&PORTLET_PARAM_SYSTEM_UUID=$uuid&PORTLET_PARAM_SYSTEM_UUID=$uuid'),
			'action_message':'portal/workflow/message.wf',
			'action_message_detail':'portal/workflow/message.wf?sid=$sid&cmd=WorkFlow_Execute_Worklist_BindReport_Open&id=$id&openstate=$openstate&task_id=$task_id',
			'action_govword':'portal/workflow/govWord.wf',
			
			'action_post':string.Template('post.php?action=newthread&fid=$fid&extra=page%3D1&topicsubmit=yes'),
			'action_seccode':string.Template('ajax.php?action=updateseccode&inajax=1'),
		}
		self.conf.update(param)
		#
		HttpClient.__init__(self, self.conf['url'], '')
		self.opener.addheaders=[('Accept-Language','zh-cn'), \
			('User-agent','Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1))')]
		self.url = self.conf['url']
		self.encoding = self.conf['encoding']
		self.image_base = self.conf['image_base']
		self.formhash = ''

	def login(self,username,password):
		content = self.request_get_simple(self.url + 'portal')
		#print content
		logindata=(('userid',username), ('pwd',password), ('PORTAL_LANG','cn'), ('cmd','Login'), ('_CACHE_LOGIN_TIME_','%d'%time.time()))
		self.action_login = self.url + self.conf['action_login'].substitute()
		content = self.request_post(self.action_login, logindata, self.conf['action_login_referer'])
		#print content
		try:
			str_re='login.wf\?sid=(.*?)&cmd='
			reObj=re.compile(str_re)
			allMatch=reObj.findall(content)
			self.sid=allMatch[0]
			print self.sid
			return True
			#print img_src
		except Exception,e:
			print e
		return False

	def getMessageList(self):
		action_msglist = self.url + self.conf['action_msglist'].substitute(sid=self.sid)
		action_msglist_referer = self.url + self.conf['action_msglist_referer'].substitute(sid=self.sid)
		content = self.request_get_simple(action_msglist, action_msglist_referer)
		#print content
		try:
			str_re='name=systemUUID value=\'([0-9a-zA-Z]+)\''
			reObj=re.compile(str_re)
			allMatch=reObj.findall(content)
			self.systemUUID=allMatch[0]
			print self.systemUUID
			#print img_src
		except Exception,e:
			print e
			return False
		#
		action_msglist2 = self.url + self.conf['action_msglist2'].substitute(sid=self.sid, uuid=self.systemUUID)
		content = self.request_get_simple(action_msglist2, action_msglist)
		#print content
		start_pos = content.find('<table ')
		end_pos = content[start_pos:].find('</table>')
		#print content[start_pos:end_pos+8]
		return content[start_pos:end_pos+8]
		return True

	def getMessagePage(self,msgid,task_id,openstate):
		action_msglist2 = self.url + self.conf['action_msglist2'].substitute(sid=self.sid, uuid=self.systemUUID)
		action_message = self.url + self.conf['action_message']
		logindata=(('sid',self.sid), ('cmd','WorkFlow_Execute_Worklist_File_Open'), ('id',msgid), ('task_id',task_id), ('openstate',openstate))
		content = self.request_post(action_message, logindata, action_msglist2)
		print content

	def testxxx(self):
		self.sid = 'yw1_1344002608081_59.56.9.96$ff6958472c644a19309f194cf5b76a53L{cn}LC{pc}C'
		content = '''
var OFFICE_OBJ_FILENAME='OFFICE_ZW.doc';
var OFFICE_OBJ_USERNAME='业务人员一';
var OFFICE_OBJ_OPENTYPE='-1,0,1,1,0,0,0,1';
var OFFICE_OBJ_ROOTDIR='WebOffice';
var OFFICE_OBJ_DIR1='174654';
var OFFICE_OBJ_DIR2='7744';
var OFFICE_OBJ_TEMPLATE_DIR='';
var OFFICE_OBJ_TEMPLATE_FILE='';
var OFFICE_OBJ_STATUS='WRITE';
var OFFICE_OBJ_OPEN_TEMPLATE_WIN=false;

'''
		try:
			print content.replace("\n",'').split(';')
			var_list = [e.replace('var ','').split('=') for e in content.replace("\n",'').split(';')]
			print var_list
			params = [('DBSTEP','DBSTEP'), ('OPTION','LOADFILE')]
			for entry in var_list:
				if len(entry) < 2:
					continue
				if (entry[0] == 'OFFICE_OBJ_FILENAME'):
					params.append(('FILENAME', entry[1][1:-1]))
					params.append(('FILETYPE', '.doc'))
				elif (entry[0] == 'OFFICE_OBJ_USERNAME'):
					params.append(('USERNAME', entry[1][1:-1]))
				elif (entry[0] == 'OFFICE_OBJ_ROOTDIR'):
					params.append(('rootDir', entry[1][1:-1]))
				elif (entry[0] == 'OFFICE_OBJ_DIR1'):
					params.append(('dir1', entry[1][1:-1]))
				elif (entry[0] == 'OFFICE_OBJ_DIR2'):
					params.append(('dir2', entry[1][1:-1]))
			params.extend([('sid',self.sid), ('fn','OFFICE_ZW.doc')])
			print params
			str_content = (chr(10)+chr(13)).join(["%s=%s"%(k,base64.b64encode(v)) for (k,v) in params])+(chr(10)+chr(13))
			print str_content
			total_content = '%-16s%-16d%-16d%-16d%s'%('DBSTEP V3.0',len(str_content),0,0,str_content)
			print total_content
		except Exception,e:
			print e
			return False

	def getMessage(self,msgid,task_id,openstate):
		action_message_detail = self.url + self.conf['action_message_detail'].substitute(sid=self.sid, id=msgid, task_id=task_id, openstate=openstate)
		action_message = self.url + self.conf['action_message']
		content = self.request_get_simple(action_message_detail, action_message)
		print content
		#
		try:
			start_pos = content.find('var OFFICE_OBJ_FILENAME')
			end_pos = content[start_pos:].find('</script>')
			print content[start_pos:end_pos]
			var_list = [e.replace('var ','').split('=') for e in content[start_pos:end_pos].replace("\n",'').split(';')]
			params = [('DBSTEP','DBSTEP'), ('OPTION','LOADFILE')]
			for entry in var_list:
				if len(entry) < 2:
					continue
				if (entry[0] == 'OFFICE_OBJ_FILENAME'):
					params.append(('FILENAME', entry[1][1:-1]))
					params.append(('FILETYPE', '.doc'))
				elif (entry[0] == 'OFFICE_OBJ_USERNAME'):
					params.append(('USERNAME', entry[1][1:-1]))
				elif (entry[0] == 'OFFICE_OBJ_ROOTDIR'):
					params.append(('rootDir', entry[1][1:-1]))
				elif (entry[0] == 'OFFICE_OBJ_DIR1'):
					params.append(('dir1', entry[1][1:-1]))
				elif (entry[0] == 'OFFICE_OBJ_DIR2'):
					params.append(('dir2', entry[1][1:-1]))
			params.extend([('sid',self.sid), ('fn','OFFICE_ZW.doc')])
			print params
			str_content = (chr(10)+chr(13)).join(["%s=%s"%(k,base64.b64encode(v)) for (k,v) in params])+(chr(10)+chr(13))
			print str_content
			total_content = '%-16s%-16d%-16d%-16d%s'%('DBSTEP V3.0',len(str_content),0,0,str_content)
			print total_content
			action_govword = self.url + self.conf['action_govword']
			content = self.request_post(action_govword, total_content)
			#
			#dbstep = content[0:16]
			overhead = int(content[16:32])
			doclen = int(content[48:64])
			#statusstr = content[64:64+overhead]
			doccontent = content[64+overhead+16:-15]
			print doclen
			print doccontent
			fileHandle = open('temp.doc', 'w')
			fileHandle.write(doccontent)
			fileHandle.close()
		except Exception,e:
			print e
			print content
			exit(1)

	def getSeccode(self,fid):
		#
		if not self.formhash:
			self._preparePost(fid)
		#
		action_seccode = self.url + self.conf['action_seccode'].substitute()
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
			'url':'http://zthf'+'tech.eic'+'p.net:180/',
			'username':'yw1',
		}
		discuz = WebOffice(param)
		discuz.testxxx()
		exit()
		discuz.login(param['username'], '123')
		discuz.getMessageList()
		exit()
#	except Exception,e:
#		print 'Error'
#		print e

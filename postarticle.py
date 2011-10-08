#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: post.py

import os
import fnmatch,sys
from discuz import Discuz

def postContentByPart(discuz,fileName,contents):
			initsize=900
			count=0
			totallen=len(contents)
			oder=0
			while count<= totallen:
				if count==0:
					#fileName=unicode(fileName,'utf-8','ignore').encode('gbk','ignore')
					fileName=fileName
				else:
					#fileName=unicode(fileName+'继'+str(oder),'utf-8','ignore').encode('gbk','ignore')
					fileName=fileName+u'继'.encode('gbk','ignore')+str(oder)
				#c=unicode(contents[count:count+initsize],'utf-8','ignore').encode('gbk','ignore')
				c=contents[count:count+initsize]
				print 'title:'+fileName+', content:'+c
				discuz.post(fid,fileName,c)
				#time.sleep(20)
				#print fileName
				#print c
				count+=initsize
				oder+=1

def postContent(forumlist,fileName,contents):
	for forum in forumlist:
		discuz = forum['object']
		fid = forum['fid']
		encoding = forum['encoding']
		if encoding == 'utf-8':
			fileName=unicode(fileName,'gbk','ignore').encode('utf-8','ignore')
			contents=unicode(contents,'gbk','ignore').encode('utf-8','ignore')
		discuz.post(fid,fileName,contents)

def postAllFile(forumlist,path):
	if(path==''):
		path='./'
		print 'null'
		return
	
	for fileName in os.listdir (path):
		if fnmatch.fnmatch ( fileName, '*.txt' ):
			print 'Posting... '+fileName
			f=open(path+fileName,"r")
			contents=f.read()
			try:
				contents = contents.decode('utf-8').encode('gbk')
			except:
				pass
			fileName=fileName.replace('.txt','')
			print 'fileName:'+fileName
			print 'len(contents):'+str(len(contents))
			postContent(forumlist,fileName,contents)
			f.close()


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage :", sys.argv[0], " <username> <password> <url> <fid>"
		exit(1)
	
	fid=0
	try:
		param = {}
		username = sys.argv[1]
		password=sys.argv[2]
		if len(sys.argv) >3:
			url=sys.argv[3]
			param['url'] = url
		if len(sys.argv)>4:
			fid=sys.argv[4]
			#print username+' '+password+' '+url+' '+fid
		forumlist = []
		discuz = Discuz(param)
		discuz.login(username,password)
		forumlist.append({'name':'discuz', 'object':discuz, 'fid':fid, 'encoding':'gbk'})
#		discuz_utf8 = Discuz({'url':'http://localhost/discuz_utf8/'})
#		discuz_utf8.login('un44444444','44444444')
#		forumlist.append({'name':'discuz_utf8', 'object':discuz_utf8, 'fid':fid, 'encoding':'utf-8'})
		print 'len(forumlist):'+str(len(forumlist))
		postAllFile(forumlist, './')
	except Exception,e:
		print 'Error'
		print e
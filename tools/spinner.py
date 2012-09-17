#!/usr/bin/env python
# encoding: UTF-8

def filt_out_non_ascii(s):
	return ''.join(c for c in s if c<chr(128))

def addslashes(s):
	#d = {"'":"\\'", "\0":"\\\0", "\\":"\\\\"}
	d = {"'":"''"}
	return ''.join(d.get(c, c) for c in s if c<chr(128))

if __name__ == '__main__':
	import time
	import sys
	sys.path.append('..')
	import common.mdb
	import poster
	spinner = poster.Poster()
	db = common.mdb.AdoMdb()
	db.OpenDataBase('R:/SpiderResult.mdb')
	#
	resultset = db.ExecuteQuery(u'select ID,标题,内容 from content WHERE spin=0 AND 已采<>0', 500)
	for record in resultset:
		result=[0,'','']
		idx = 0
		for j in record:
			if isinstance(j, unicode):
				result[idx]=j.encode('utf8')
				result[idx]=filt_out_non_ascii(result[idx])
			else:
				result[idx]=j
			idx+=1
		#print result
		print 'begin ID=%d' % result[0]
		
		#title
		time.sleep(1)
		title = spinner.spin_content(result[1])
		if title == 'except':
			print "title except"
			continue
		elif title[:6] == 'error=':
			print "title return(%s)"%title
			break
		print result[1]
		print title
		
		#content
		time.sleep(1)
		content = spinner.spin_content(result[2])
		if content == 'except':
			print "content except"
			continue
		elif content[:6] == 'error=':
			print "content return(%s)"%content
			break
		#print result[2]
		#print content
		
		#update
		title = addslashes(title)
		content = addslashes(content).encode('utf8')
		db.ExecuteUpdate(u"update content set 标题='%s',内容='%s',spin=1 where ID=%d" % (title, content, result[0]))
		print 'complete ID=%d' % result[0]
	db.CloseDatabase()
	print spinner.query_times()

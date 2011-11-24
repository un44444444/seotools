#!/usr/bin/env python
# encoding: UTF-8

def addslashes(s):
	#d = {"'":"\\'", "\0":"\\\0", "\\":"\\\\"}
	d = {"'":"''"}
	return ''.join(d.get(c, c) for c in s if c<chr(128))

if __name__ == '__main__':
	import time
	import mdb
	import poster
	spinner = poster.Poster()
	db = mdb.AdoMdb()
	db.OpenDataBase('R:/SpiderResult.mdb')
	#
	resultset = db.ExecuteQuery(u'select ID,标题,内容 from content WHERE spin=0', 500)
	for record in resultset:
		result=[0,'','']
		idx = 0
		for j in record:
			if isinstance(j, unicode):
				#result[idx]=j.encode('cp936')
				result[idx]=j
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
		elif title == 'error=You have reached the daily limit!':
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
		elif content == 'error=You have reached the daily limit!':
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

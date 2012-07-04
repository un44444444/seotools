#!/usr/bin/env python
# encoding: UTF-8

def filt_out_non_ascii(s):
	return ''.join(c for c in s if c<chr(128))

def addslashes(s):
	#d = {"'":"\\'", "\0":"\\\0", "\\":"\\\\"}
	d = {"'":"''"}
	return ''.join(d.get(c, c) for c in s if c<chr(128))

if __name__ == '__main__':
	import mdb
	db = mdb.AdoMdb()
	db.OpenDataBase('R:/#%20963e007635a3753a011f.mdb')
	#
	last_time = None
	resultset = db.ExecuteQuery(u'SELECT Min(log_id) FROM blog_Article', 1)
	max_fixtime_id = int(resultset[0][0])
	resultset = db.ExecuteQuery(u'SELECT log_id,log_title,log_posttime FROM blog_Article WHERE log_id>%d'%max_fixtime_id, 500)
	for record in resultset:
		atricle_id = int(record[0])
		atricle_title = record[1]
		atricle_time = record[2]
		print 'begin ID=%d' % atricle_id
		print 'begin Title=%s' % atricle_title
		print 'begin Time=%s' % atricle_time
		atricle_title = atricle_title.replace('&nbsp;', ' ').replace('&lt;', '<').replace('&gt;', '>')
		title_peice = atricle_title.split('_')
		if len(title_peice) > 1:
			atricle_title = '_'.join(title_peice[:-1])
		print 'begin new Title=%s' % atricle_title
		#time determine update
		if last_time is not None and (atricle_time-last_time).days<1:
			db.ExecuteUpdate(u"UPDATE blog_Article SET log_title='%s',log_intro='',log_posttime=log_posttime+%d WHERE log_id=%d" % (atricle_title, atricle_id-max_fixtime_id+1, atricle_id))
		else:
			db.ExecuteUpdate(u"UPDATE blog_Article SET log_title='%s',log_intro='',log_posttime=log_posttime+1 WHERE log_id=%d" % (atricle_title, atricle_id))
			max_fixtime_id = atricle_id
		last_time = atricle_time
		print 'complete ID=%d' % atricle_id
	#
	db.CloseDatabase()

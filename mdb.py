#!/usr/bin/env python
# encoding: UTF-8

import adodbapi

class AdoMdb:
	def __init__(self):
		pass
	
	def OpenDataBase(self,filepath):
		try:
			constr = 'Provider=Microsoft.Jet.OLEDB.4.0;Data Source=%s' % filepath
			#print constr
			#tell the server  we are not planning to update...
			adodbapi.adodbapi.defaultIsolationLevel = adodbapi.adodbapi.adXactBrowse
			#and we want a local cursor (so that we will have an accurate rowcount)
			adodbapi.adodbapi.defaultCursorLocation = adodbapi.adodbapi.adUseClient
			self.conn=adodbapi.connect(constr)
			self.cur=self.conn.cursor()
		except:
			print 'open database error'
			return False
		return True
	
	def GetAllColName(self,tablename):
		try:
			sql = 'select * from '+tablename
			print sql
			self.cur.execute(sql)
			self.colnamelist=[]
			#print type(self.cur.description)
			for name in self.cur.description:
				self.colnamelist.append(name[0])
				#print name[0]
		except:
			print 'Get ColName error'
			return []
		return self.colnamelist

	def QueryTable(self,sql,showraw=100):
		records = []
		try:
			self.cur.execute(sql)
			print 'rowcount =',self.cur.rowcount
			records = self.cur.fetchmany(showraw)
		except:
			print 'Query table error'
		return records
	
	def CloseDatabase(self):
		try:
			self.cur.close()
			self.conn.close()
		except:
			print 'Close Database error'


if __name__ == '__main__':
	db=AdoMdb()
	db.OpenDataBase('R:/SpiderResult.mdb')
	#list=db.GetAllColName('content')
	#print list
	db = db.QueryTable(u'select ID,标题 from content', 2)
	for i in db:
		result=""
		for j in i:
			if isinstance(j, unicode):
				j=j.encode('cp936')
			elif not isinstance(j, str):
				j=str(j)
			result=result+j+' '
		print result

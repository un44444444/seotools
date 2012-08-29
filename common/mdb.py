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
			#tell the server we are not planning to update...
			#adodbapi.adodbapi.defaultIsolationLevel = adodbapi.adodbapi.adXactBrowse
			#we are planning to update...
			adodbapi.adodbapi.defaultIsolationLevel = adodbapi.adodbapi.adXactReadCommitted
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
	
	def GetRecordCount(self,sql):
		try:
			self.cur.execute(sql)
			return self.cur.rowcount
		except:
			print 'Get record count error'
		return 0
	
	def ExecuteQuery(self,sql,showraw=100):
		records = []
		try:
			self.cur.execute(sql)
			#print 'rowcount =',self.cur.rowcount
			records = self.cur.fetchmany(showraw)
		except:
			print 'Execute query table error'
		return records
	
	def ExecuteUpdate(self,sql):
		try:
			self.cur.execute(sql)
			self.conn.commit()
		except:
			print 'Execute update table error'
	
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
	resultset = db.ExecuteQuery(u'select ID,标题 from content', 2)
	for record in resultset:
		result=""
		for j in record:
			if isinstance(j, unicode):
				j=j.encode('cp936')
			elif not isinstance(j, str):
				j=str(j)
			result=result+j+' '
		print result
	#update
	db.ExecuteUpdate(u"update content set 标题='custom title by python' where ID=2")

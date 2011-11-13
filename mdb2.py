#!/usr/bin/env python
# encoding: UTF-8

import adodbapi

class DBTestor:
	def __init__(self):
		self.conn = None
		
	def __del__(self):
		try:
			self.conn.close()
		except:
			pass
		
	def connectDB(self, connectString):
		self.conn = adodbapi.connect(connectString)
		
	def closeDB(self):
		self.conn.close()
		
	def fielddict(self, cursor):
		dict = {}
		i = 0
		for field in cursor.description:
			dict[field[0]] = i
			i += 1
		return dict
	
	def testCommand(self):
		u"测试执行SQL命令，及参数、事务"
		cursor = self.conn.cursor()
		sql = """if exists (select * from sysobjects where id = object_id(N'Demo_Table') and OBJECTPROPERTY(id, N'IsUserTable') = 1)
					Drop Table Demo_Table;
				CREATE TABLE Demo_Table (
				   ID int IDENTITY (1, 1) NOT NULL ,
				   Name varchar(50) NOT NULL Default('')
				   PRIMARY KEY  CLUSTERED 
				   (
					   [ID ]
				   )
			   );"""
		cursor.execute(sql)

		sql = """INSERT INTO Demo_Table (Name) VALUES (?);"""
		cursor.execute(sql, ("jame",))
		sql = """INSERT INTO Demo_Table (Name) VALUES (?);"""
		cursor.execute(sql, ("jame2",))

		sql = """SELECT @@Identity;"""
		cursor.execute(sql)
		print "Inserted new record's ID = %s" % cursor.fetchone()[0]
		
		cursor.close()
		
		#默认对数据库进行修改后必须要提交事务，否则关闭数据库时会回滚
		self.conn.commit()

	
	def testQuery(self):
		u"测试查询功能，通过序号和字段名读取数据"
		cursor = self.conn.cursor()
		cursor.execute("SELECT * FROM authors")
		try:
			fields = self.fielddict(cursor)
			row = cursor.fetchone()
			while row != None:
				print "%s: %s %s" % (row[0], row[fields['au_fname']], row[fields['au_fname']])
				row = cursor.fetchone()					
		finally:
			cursor.close()
			

	def testStoreProc(self):
		u"测试存储过程功能"
		cursor = self.conn.cursor()
		sql = """if exists (select * from sysobjects where id = object_id(N'insert_data_demo') and OBJECTPROPERTY(id, N'IsProcedure') = 1)
					Drop Procedure insert_data_demo;"""
		cursor.execute(sql)
		sql = """CREATE PROCEDURE INSERT_DATA_Demo
					@Name varchar(50),
					@ID int output
				 AS
					INSERT INTO Demo_Table (Name) VALUES (@Name);
					Select @ID = @@Identity;"""
		cursor.execute(sql)
		
		(name, id) = cursor.callproc("insert_data_demo", ("tom", 0))				
		print "Inserted new record's ID = %i" % id
		
		sql = """SELECT * FROM Demo_Table;"""
		cursor.execute(sql)
		print cursor.fetchall()		
		cursor.close()
		
		self.conn.commit()
		
				
if __name__ == "__main__":
	test = DBTestor()
	test.connectDB("Provider=SQLOLEDB.1;Persist Security Info=True;Password=;User ID=sa;Initial Catalog=pubs;Data Source=.")
	try:
		test.testQuery()
		test.testCommand()
		test.testStoreProc()		
	finally:
		test.closeDB()

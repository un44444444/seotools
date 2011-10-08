#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Filename: filemgr.py

import sqlite3

class FileMgr:
	def __init__(self):
		self.conn = sqlite3.connect('sample.db')
		self.curs = self.conn.cursor()
		# Create catelog table
		self.curs.execute('''CREATE TABLE IF NOT EXISTS catelog(
			id INTEGER PRIMARY KEY AUTOINCREMENT, 
			parent_id INTEGER DEFAULT 0, 
			name TEXT, 
			create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
		''')

	def __exit__(self):
		self.curs.close()
		self.conn.close()

	def query_all_record(self, table_name):
		#
		self.curs.execute("SELECT * FROM "+table_name)
		for row in self.curs:
			print row

	def add_catelog(self, catelog_name, parent_id=0):
		self.curs.execute("INSERT INTO catelog(parent_id, name) VALUES \
			("+str(parent_id)+",'"+catelog_name+"')")
		self.conn.commit()
		return self.curs.lastrowid

	def get_catelogs(self, parent_id=0):
		#print "get_catelogs("+str(parent_id)+")"
		cursor = self.conn.cursor()
		cursor.execute("SELECT id,parent_id,name FROM catelog WHERE parent_id="+str(parent_id)+" ORDER BY id ASC")
		catelogs = []
		for row in cursor:
			#print row
			catelog = dict(zip(('id', 'parent_id', 'name'), row))
			catelog['childs'] = self.get_catelogs(catelog['id'])
			catelogs.append(catelog)
		#
		cursor.close()
		return catelogs


if __name__ == "__main__":
	filemgr = FileMgr()
#	catelog_id = filemgr.add_catelog('目录1')
#	catelog_id = filemgr.add_catelog('子目录1', catelog_id)
#	filemgr.query_all_record('catelog')
	catelogs = filemgr.get_catelogs()
	print catelogs

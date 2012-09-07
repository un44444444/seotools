#!/usr/local/bin/python
# coding: utf-8
import os
import ConfigParser


class Configuration(object):
	def __init__(self):
		self.__cp = ConfigParser.ConfigParser()
		self.__sections = {}
		self._write_config_back = False
	def load(self, cfgfile):
		self.cfgfile = cfgfile
		if not os.path.isfile(self.cfgfile):
			os.rename(self.cfgfile+'.default', self.cfgfile)
		self.__cp.read(self.cfgfile)
		#print self.__cp.sections()
	def __del__(self):
		#print self._write_config_back
		if self._write_config_back:
			fp=open(self.cfgfile, 'w')
			self.__cp.write(fp)
			fp.close()
	
	def __getattr__(self, name):
		#print 'Configuration.__getattr__(%s)'%name
		if self.__sections.has_key(name):
			return self.__sections[name]
		if self.__cp.has_section(name):
			section = Section(self.__cp, name)
			self.__sections[name] = section
			return section
		#raise Exception('section(%s) not exist'%(name))
		raise AttributeError
	
config = Configuration()

class Section(object):
	def __init__(self, cp, name):
		self.__cp = cp
		self.__name = name
		self.__options = {}
		#print self.__cp.options(self.__name)
	
	def __getattr__(self, name):
		#print 'Section.__getattr__(%s)'%name
		if self.__options.has_key(name):
			return self.__options[name]
		if self.__cp.has_option(self.__name, name):
			value = self.__cp.get(self.__name, name)
			self.__options[name] = value
			return value
		#raise Exception('option(%s) not exist in section(%s)'%(name, self.__name))
		raise AttributeError
	def __setattr__(self, name, value):
		#print 'Section.__setattr__(%s, %s)'%(name, value)
		if not self.__dict__.has_key('_Section__options'):
			return object.__setattr__(self, name, value)
		is_option = False
		if self.__options.has_key(name):
			is_option = True
		elif self.__cp.has_option(self.__name, name):
			is_option = True
		if is_option:
			self.__cp.set(self.__name, name, value)
			self.__options[name] = value
			global config
			config._write_config_back = True
			#print config._write_config_back
			return
		return object.__setattr__(self, name, value)

if __name__ == "__main__":
	#global config
	config.load('seotools.ini')
	print dir(config)
	print config.lusongsong
	print config.lusongsong.filedir
	config.lusongsong.filedir = 'lusongsong_filedir'
	print config.lusongsong.filedir
	print config.queryexlink.time
	config.queryexlink.time = 8888
	print config.queryexlink.time
	print config.lusongsong.time
	config.lusongsong.time = 9999
	print config.lusongsong.time

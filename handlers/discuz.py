#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filename: discuz.py

import re

import sys
sys.path.append('..')
from common.http import HttpClient

class DiscuzBase(HttpClient):
	def __init__(self):
		conf = self.conf
		HttpClient.__init__(self, conf['url'], conf['username'])

	def get_error_message(self,content):
		p = re.compile('<div\s*id="messagetext"\s*class="alert_error"\s*>\s*<p>(.*?)\s*<script\s*')
		m = p.findall(content)
		if len(m) > 0:
			#for i in m:
			#	print  i.replace('</p>','').decode(self.encoding,'ignore')
			return m[0].replace('</p>','')
		else:
			return ''


if __name__ == "__main__":
	pass

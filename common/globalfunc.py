#!/usr/bin/env python
# encoding: UTF-8

try:
	import json
except ImportError:
	import simplejson as json
import web
from web.contrib.template import render_mako


render = render_mako(
	directories=['templates'],
	input_encoding='utf8',
	output_encoding='utf8',
)

def jsonize(func):
	def _(*a, **kw):
		ret = func(*a, **kw)
		web.header('Content-Type', 'application/json')
		return json.dumps(ret)
	return _

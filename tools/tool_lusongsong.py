#!/usr/bin/env python
# encoding: UTF-8
import os
import webbrowser

def deal_a_site(site, time=20):
	prefix = 'http://luson'+'gsong.com'
	postfix = '&submit=%BF%AA%CA%BC%BD%F8%D0%D0%B7%E8%BF%F1%B5%C4%D0%FB%B4%AB%B0%C9%A3%A1'
	dest_url = '%s/tool/seo/seo.asp?url=%s&auto=yes&ttime=%d%s' % (prefix, site, time, postfix)
	webbrowser.open_new_tab(dest_url)

def kill_all_iexplorer():
	# only for windows
	os.system('taskkill /F /IM iexplore.exe')


if __name__ == '__main__':
	deal_a_site('www.chen-w.com')

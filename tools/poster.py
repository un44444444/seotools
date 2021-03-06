#!/usr/bin/env python
# encoding: UTF-8

import urllib2
import time

class Poster:
	def __init__(self):
		self.index = -1
		self.opener = urllib2.build_opener()
		self._change_action()
		
	def _change_action(self):
		host = ''.join(['http://api.','spinner','chief','.com'])
		port = 9001
		config = [
				#('4039a8ef565c4f5d8', ''.join(['un','4444','44441']), '444444441'),
				#('45a0a23babbd44729', ''.join(['un','4444','4444']), '44444444'),
				('753a2d8b9995450e8', ''.join(['ray','mond','182']), '2198300'),
		]
		proxies = [
				#'80.58.250.68:80',
				#'203.172.188.34:80',
				'186.113.26.36:3128',
		]
		if self.index >= (len(config)-1):
			return False
		self.index += 1
		(apikey,username,password) = config[self.index]
		proxy_handler = urllib2.ProxyHandler({'http': proxies[self.index]})
		self.opener = urllib2.build_opener(proxy_handler)
		self.opener.addheaders=[('User-agent','Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)')]
		action = '%s:%d/apikey=%s&username=%s&password=%s' % (host, port, apikey, username, password)
		#protect_words = 'cubic,zirconia,wholesale,rings,earring,gemstone,synthetic'
		protect_words = 'lose weight,lose,Lose,weight,Weight'
		self.action_spin = action + '&spintype=1&spinfreq=1&original=1&protecthtml=1&protectwords=' + protect_words
		self.action_times = action + '&querytimes=2'
		return True
	
	def spin_content(self, data):
		result = self._post_data(self.action_spin, data)
		if result == 'error= query time reach limit':
			if self._change_action():
				result = self._post_data(self.action_spin, data)
		return result
	
	def query_times(self):
		print self.action_times
		return self._post_data(self.action_times, '')
	
	def _post_data(self, action, data, retry_count=3):
		err_count = 0
		flage = True
		while flage:
			try:
				req=urllib2.Request(action,data)
				resp=self.opener.open(req, timeout=20)
				content=resp.read()
				flage=False
				return content
			except:
				if err_count >= retry_count:
					break
				err_count += 1
				print "Wait for 2 seconds..."
				time.sleep(2)
		#
		return 'except'
	
	def _get_data(self, action):
		try:
			req=urllib2.Request(action)
			resp=self.opener.open(req)
			content=resp.read()
			return content
		except:
			return 'except'

if __name__ == '__main__':
	poster = Poster()
#	data = "<p><p><p>Cubic Zirconia, it was in the form of poly-crystalline ceramic, used as a refractory material. The cubic zirconia was perfectly invented in former Soviet Union in 1973 and the mass commercial production began in 1976. It became popular in 1980 and had reached 10 tons of global production.<p>Cubic Zirconia is known as low cost synthetic diamond which is close visual likeness to diamond and it was founded since 1976. The synthesized material is relatively hard, slightly harder than the most semi-precious gems. Its dispersion is very high, even higher than diamond. It is usually colorless (It may be made in different vary colors) but it change to other colors under shortwave or longwave UV such as yellow, greenish yellow, beige and whitish.<p>In recent years, the jewelry manufacturers have sought ways to improve cubic zirconia. The CZ's coating of diamond-like carbon is one of such innovation. The resulting material overall is harder, more lustrous and more like diamond. Its refractive index is improved thus making it appear more like diamond.<p>Today, you may easily shop around your favorite cubic zirconia jewelry through online jewelry stores and there are lots choices in terms of categories, patterns, styles as well as prices. Affordable prices on fashion jewelry, costume jewelry, jewelry accessories, all at Casjewellery.com <br>http://www.casjewellery.com/newshow-135.html<br>www.CASJewellery.com has become a global costume jewelry wholesaler since 2008; we serve customers all over the world and the growth still ascending. Whether you are a wholesaler or a shopper looking for the latest products, we are treating impartially to offer the same lowest price to all. For years, we had never changed our faith, to provide experience professional services and maintain the products in high quality standard are our most important task to achieve.<p>My business scope include a variety product range of body piercing jewelry , pendants, bead jewelry, rhinestone jewelry, pearl jewelry. Cubic zirconia jewelry costume jewelry. Simultaneously we maintain good and stable co operations with our manufacturers and therefore our price is definitively competitive in the market. You do not have to worry and time wasting to search the products, all you need to do is enter to our online purchase website. <p>Our corporate culture: coordination, cooperation, enthusiasm and sincere. <p>Business advantages: superior quality, innovative style, low price, which won a high recognition from our customers. All products are taken the same in pictures, so you can be assured of the quality of our products.<p>Business objectives: We do our utmost to cooperate with our partners to establish a close and mutually beneficial relationship base on equality thus to build up a good reputation and credibility to win the utmost trusty. <p>Enterprise��s goal: We do the best to establish a closely, mutually beneficial relations with our co-operator and to win a good prestige and good faith as well.<br>Enterprise��s idea: Sincere, mutual benefits. Our customer supporting is our best motivation. We rigid to provide the most satisfied products and the service conscientiously to all our customers.<br>"
#	result = poster.spin_content(data)
#	print result
#	time.sleep(1)
	result = poster.query_times()
	print result

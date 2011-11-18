#!/usr/bin/env python
# encoding: UTF-8

import urllib2

class Poster:
	def __init__(self):
		port = 8080
		apikey = '45a0a23babbd44729'
		username = 'un44444444'
		password = '44444444'
		action = 'http://api.spinnerchief.com:%d/?apikey=%s&username=%s&password=%s' % (port, apikey, username, password)
		self.action_spin = action + '&spintype=1&spinfreq=1&original=1&protecthtml=1&protectwords=cubic,zirconia,wholesale,rings,earring,gemstone,synthetic'
		self.action_times = action + '&querytimes=2'
	
	def spin_content(self, data):
		return self._post_data(self.action_spin, data)
	
	def query_times(self):
		return self._post_data(self.action_times, '')
	
	@staticmethod
	def _post_data(action, data):
		try:
			req=urllib2.Request(action,data)
			resp=urllib2.urlopen(req)
			content=resp.read()
			return content
		except:
			return 'except'
	
	@staticmethod
	def _get_data(action):
		try:
			req=urllib2.Request(action)
			resp=urllib2.urlopen(req)
			content=resp.read()
			return content
		except:
			return 'except'

if __name__ == '__main__':
	poster = Poster()
	data = "<p><p><p>Cubic Zirconia, it was in the form of poly-crystalline ceramic, used as a refractory material. The cubic zirconia was perfectly invented in former Soviet Union in 1973 and the mass commercial production began in 1976. It became popular in 1980 and had reached 10 tons of global production.<p>Cubic Zirconia is known as low cost synthetic diamond which is close visual likeness to diamond and it was founded since 1976. The synthesized material is relatively hard, slightly harder than the most semi-precious gems. Its dispersion is very high, even higher than diamond. It is usually colorless (It may be made in different vary colors) but it change to other colors under shortwave or longwave UV such as yellow, greenish yellow, beige and whitish.<p>In recent years, the jewelry manufacturers have sought ways to improve cubic zirconia. The CZ's coating of diamond-like carbon is one of such innovation. The resulting material overall is harder, more lustrous and more like diamond. Its refractive index is improved thus making it appear more like diamond.<p>Today, you may easily shop around your favorite cubic zirconia jewelry through online jewelry stores and there are lots choices in terms of categories, patterns, styles as well as prices. Affordable prices on fashion jewelry, costume jewelry, jewelry accessories, all at Casjewellery.com <br>http://www.casjewellery.com/newshow-135.html<br>www.CASJewellery.com has become a global costume jewelry wholesaler since 2008; we serve customers all over the world and the growth still ascending. Whether you are a wholesaler or a shopper looking for the latest products, we are treating impartially to offer the same lowest price to all. For years, we had never changed our faith, to provide experience professional services and maintain the products in high quality standard are our most important task to achieve.<p>My business scope include a variety product range of body piercing jewelry , pendants, bead jewelry, rhinestone jewelry, pearl jewelry. Cubic zirconia jewelry costume jewelry. Simultaneously we maintain good and stable co operations with our manufacturers and therefore our price is definitively competitive in the market. You do not have to worry and time wasting to search the products, all you need to do is enter to our online purchase website. <p>Our corporate culture: coordination, cooperation, enthusiasm and sincere. <p>Business advantages: superior quality, innovative style, low price, which won a high recognition from our customers. All products are taken the same in pictures, so you can be assured of the quality of our products.<p>Business objectives: We do our utmost to cooperate with our partners to establish a close and mutually beneficial relationship base on equality thus to build up a good reputation and credibility to win the utmost trusty. <p>Enterprise¡¯s goal: We do the best to establish a closely, mutually beneficial relations with our co-operator and to win a good prestige and good faith as well.<br>Enterprise¡¯s idea: Sincere, mutual benefits. Our customer supporting is our best motivation. We rigid to provide the most satisfied products and the service conscientiously to all our customers.<br>"
	result = poster.spin_content(data)
	print result
	import time
	time.sleep(1)
	result = poster.query_times()
	print result

import scrapy
import base64
import random
import string
import uuid
import os.path

class BrickSetSpider(scrapy.Spider):
	name = 'brick_spider'
	start_urls = ['http://www.nationalpost.com/m/index.html']
	BASE_URL = 'http://www.nationalpost.com'
	def parse(self, response):
		links = response.xpath('//p/a[@class="fc"]/@href').extract()
		for link in links:
			absolute_url = self.BASE_URL + link
			yield scrapy.Request(absolute_url, callback=self.save_file)
	def save_file(self, response):
		filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))+'.html'
		with open(os.path.join('C:/Users/panos/Desktop/Projectino/ScrapedFiles', filename), 'wb') as f:
			f.write(response.body)
			
	

		

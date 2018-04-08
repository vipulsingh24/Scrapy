# -*- coding: utf-8 -*-
import scrapy

class MyItem(scrapy.Item):
	Name = scrapy.Field()
	Language = scrapy.Field()	

class IndianNewspaperSpider(scrapy.Spider):

	name = 'indian_newspaper'
	# allowed_domains = ['https://en.wikipedia.org/wiki/List_of_newspapers_in_India']
	start_urls = ['https://en.wikipedia.org/wiki/List_of_newspapers_in_India/']

# response.xpath('//table/tr/td/i/a').extract() 
# response.xpath('//table/tr/td[2]').extract()
	
	def parse(self, response):
		sel_link = response.xpath('//table/tr')
		item = MyItem()
		for data in sel_link:
			item['Name'] = data.xpath('//td/i/a/text()').extract()
			item['Language'] = data.xpath('//td[2]/text()').extract()
		yield item	

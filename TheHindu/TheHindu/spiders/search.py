# -*- coding: utf-8 -*-
import scrapy

class SearchSpider(scrapy.Spider):

	name = 'search'
	allowed_domains = ['www.thehindu.com/archive/']
	start_urls = ['http://www.thehindu.com/archive//']

	def parse(self, response):
		sel_link = response.xpath('//a[((contains(@href, 2009)) and (contains(@href, "print"))) or\
 ((contains(@href, 2010)) and (contains(@href, "print")))]')
		for link in sel_link:
			yield {
					'link':link.xpath('@href').extract()
				}

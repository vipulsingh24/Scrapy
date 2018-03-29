# -*- coding: utf-8 -*-
import scrapy

class MonthSpider(scrapy.Spider):
	name = 'month'
	allowed_domains = ['www.thehindu.com']
	start_urls = ['http://www.thehindu.com/archive//']

	def parse(self, response):
		sel_link = response.xpath('//a[((contains(@href, 2009)) and (contains(@href, "print"))) or\
 ((contains(@href, 2010)) and (contains(@href, "print")))]/@href').extract()
		for link in sel_link:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_month)

	def parse_month(self, response):
		sel_month_link = response.css('.archiveTable tbody a')
		for link in sel_month_link:
			yield {
					'link':link.xpath('@href').extract()
				}

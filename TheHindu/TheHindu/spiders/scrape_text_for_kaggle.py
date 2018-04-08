# -*- coding: utf-8 -*-
import scrapy

class MyItem(scrapy.Item):
	link = scrapy.Field()
	headline = scrapy.Field()
	text = scrapy.Field()

class ScrapeTextSpider(scrapy.Spider):
	
	name = 'scrape_text_all'
	allowed_domains = ['www.thehindu.com']
	start_urls = ['http://www.thehindu.com/archive/']

	def parse(self, response):
		sel_link = response.xpath('//a[(contains(@href, "web"))]/@href').extract()
		for link in sel_link:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_month)


	def parse_month(self, response):
		sel_month_link = response.css('.archiveTable tbody a::attr(href)').extract()
		for link in sel_month_link:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_days)


	def parse_days(self, response): 	
		sel_article = response.xpath('//div/section/div/div/div/div/ul/li/a/@href').extract()
		for link in sel_article:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_article)


	def parse_article(self, response):
		item = MyItem()
		item['link'] = response.url
		item['headline'] = response.xpath('//div[@class="article"]/h1[@class="title"]/text()').extract()
		if ( response.xpath('//div[@class="article"]/div[5][@class="lead-img-cont"]').extract() or\
			(response.xpath('//div[@class="article"]/div[5][@class="lead-img-cont lead-img-verticle"]').extract())):
			item['text'] = response.xpath('//div[@class="article"]/div[8]/p/text()').extract()
		else:
			item['text'] = response.xpath('//div[@class="article"]/div[7]/p/text()').extract()
		yield item

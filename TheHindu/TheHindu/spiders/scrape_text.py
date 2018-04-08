# -*- coding: utf-8 -*-
import scrapy

class MyItem(scrapy.Item):
	link = scrapy.Field()
	headline = scrapy.Field()
	text = scrapy.Field()

class ScrapeTextSpider(scrapy.Spider):
	
	name = 'scrape_text'
	allowed_domains = ['www.thehindu.com']
	start_urls = ['http://www.thehindu.com/archive/']

	def parse(self, response):
		sel_link = response.xpath('//a[((contains(@href, 2009)) and (contains(@href, "print"))) or\
 ((contains(@href, 2010)) and (contains(@href, "print")))]/@href').extract()
		for link in sel_link:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_month)


	def parse_month(self, response):
		sel_month_link = response.css('.archiveTable tbody a::attr(href)').extract()
		for link in sel_month_link:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_days)


#	def parse_days(self, response):
#		item = MyItem()
#		sel_article = response.xpath('//div/section/div/div/div/div/ul/li/a[(contains(text(), "HIV")) or (contains(text(), "AIDS"))]')
#		sel_article = response.xpath('//div/section/div/div/div/div/ul/li/a[(contains(text(), " HIV ")) or\
# (contains(text(), "HIV ")) or (contains(text(), " HIV")) or (contains(text(), " HIV/")) or (contains(text(), " /HIV"))]')
#		for link in sel_article:
#			item['link'] = link.xpath('@href').extract(),
#			item['headline'] = link.xpath('text()').extract()
#	
#		sel_link = sel_article.xpath('@href').extract()
#		
#		for link in sel_link:
#			request = scrapy.Request(response.urljoin(link), callback=self.parse_article)
#			request.meta['item'] = item
#			yield request


#	def parse_article(self, response):
#		item = response.meta['item']
#		item['text'] = response.xpath('//p/text()').extract()
#		yield item
#
#
	def parse_days(self, response): 	
		sel_article = response.xpath('//div/section/div/div/div/div/ul/li/a[(contains(text(), "HIV")) or (contains(text(), "AIDS"))]').extract()
		for link in sel_article:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_article)


	def parse_article(self, response):
		item = MyItem()
		item['link'] = response.url
		item['headline'] = response.xpath('//div[@class="article"]/h1[@class="title"]/text()').extract()
		if ( response.xpath('//div[@class="article"]/div[5][@class="lead-img-cont"]').extract() or\
			(response.xpath('//div[@class="article"]/div[5][@class="lead-img-cont lead-img-verticle"]').extract())):
			item['text'] = response.xpath('//div[@class="article"]/div[7]/p/text()').extract()
		else:
			item['text'] = response.xpath('//div[@class="article"]/div[6]/p/text()').extract()
		yield item

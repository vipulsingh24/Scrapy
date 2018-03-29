# -*- coding: utf-8 -*-
import scrapy

class ScrapeTextSpider(scrapy.Spider):
	
	name = 'try_1'
	allowed_domains = ['www.thehindu.com']
	start_urls = ['http://www.thehindu.com/archive/print/2009/01/']

	def parse(self, response):
		sel_month_link = response.css('.archiveTable tbody a::attr(href)').extract()
		for link in sel_month_link:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_days)


	def parse_days(self, response):
		sel_article = response.xpath('//div/section/div/div/div/div/ul/li/a[(contains(text(), " HIV ")) or\
 (contains(text(), "HIV ")) or (contains(text(), " HIV.")) or (contains(text(), " HIV/")) or (contains(text(), " /HIV"))]')

		for link in sel_article:
			yield {
					'link':link.xpath('@href').extract(),
					'headline':link.xpath('text()').extract(),
				}
		sel_link = sel_article.xpath('@href').extract()
		for link in sel_link:
			yield scrapy.Request(response.urljoin(link), callback=self.parse_article)	

	def parse_article(self, response):
		sel_article = response.xpath('//p')
		for texts in sel_article:
			yield {
					'text':texts.xpath('text()').extract()
				}

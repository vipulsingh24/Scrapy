import scrapy

class MyItem(scrapy.Item):
	link = scrapy.Field()
	headline = scrapy.Field()
	text = scrapy.Field()

class ScrapeTextSpider(scrapy.Spider):
	
	name = 'try_2'
	allowed_domains = ['www.thehindu.com']
	start_urls = ['http://www.thehindu.com/archive/print/2009/01/01/']

	def parse(self, response):
		item = MyItem()
			
		sel_article = response.xpath('//div/section/div/div/div/div/ul/li/a[(contains(text(), " HIV ")) or\
 (contains(text(), "HIV ")) or (contains(text(), " HIV.")) or (contains(text(), " HIV/")) or (contains(text(), " /HIV"))]')

		for link in sel_article:
			item['link'] = link.xpath('@href').extract(),
			item['headline'] = link.xpath('text()').extract()

		sel_link = sel_article.xpath('@href').extract()
		for link in sel_link:
			request = scrapy.Request(response.urljoin(link), callback=self.parse_article)

		request.meta['item'] = item
		yield request

	def parse_article(self, response):
		item = response.meta['item']
		item['text'] = response.xpath('//p/text()').extract()
		yield item

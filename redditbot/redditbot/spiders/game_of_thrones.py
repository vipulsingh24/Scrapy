import scrapy

class RedditbotSpider(scrapy.Spider):
	name = 'redditbot'
	start_urls = ['http://www.reddit.com/r/gameofthrones/']

	def parse(self, response):
		titles = response.css('.title.may-blank::text').extract()
		votes = response.css('.score.unvoted::text').extract()
		time = response.css('time::attr(title)').extract()
		comments = response.css('.comments::text').extract()

		for item in zip(titles, votes, time, comments):
			scraped_info = {
							'title': item[0],
							'votes': item[1],
							'time': item[2],
							'comments': item[3]
							}
		yield scraped_info
		#return scraped_info

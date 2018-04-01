import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exporters import CsvItemExporter
from scrapy.utils.project import get_project_settings

class MyItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    # tags = scrapy.Field()

class ScrapeArticle(scrapy.Spider):
    name = 'article'
    start_urls = [
        'http://quotes.toscrape.com',
    ]

    def parse(self, response):
        quote = response.xpath('//div[@class="quote"]')

        texts = quote.xpath('//span[@class="text"]/text()').extract()
        texts = [text.strip().split(',') for text in texts]

        authors = quote.xpath('//small[@class="author"]/text()').extract()
        authors = [author.strip().split(',') for author in authors]

        # tags = quote.xpath('//div[@class="tags"]/a[@class="tag"]/text()').extract()
        # tags = [tag.strip().split(',') for tag in tags]

        result = zip(texts, authors)
        for texts, authors in result:
            item = MyItem()
            item['text'] = texts
            item['author'] = authors
            # item['tags'] = tags
            yield item


class MyItemCSVExporter(CsvItemExporter):
    def serialize_field(self, field, text, author):
        return super(MyItem, self).serialize_field(field, text, author)

# process = CrawlerProcess()

settings = get_project_settings()
settings.overrides['FEED_URI'] = 'quotes_scrape.csv'
settings.overrides['FEED_FORMAT'] = 'csv'

process = CrawlerProcess(settings)
process.crawl(ScrapeArticle)
process.start()


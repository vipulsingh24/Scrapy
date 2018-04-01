import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.exporters import CsvItemExporter
from scrapy.utils.project import get_project_settings

class MyItem(scrapy.Item):
    text = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()

class ScrapeArticle(scrapy.Spider):
    name = 'article'
    start_urls = [
        'http://quotes.toscrape.com/',
    ]

    def parse(self, response):
        item = MyItem()
        for quote in response.xpath('//div[@class="quote"]'):
                item['text'] = quote.xpath('//span[@class="text"]/text()').extract(),
                item['author'] = quote.xpath('//small[@class="author"]/text()').extract(),
                item['tags'] = quote.xpath('//div[@class="tags"]/a[@class="tag"]/text()').extract()
        yield item

        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

class MyItemCSVExporter(CsvItemExporter):
    def serialize_field(self, field, text, author, tags):
        return super(MyItem, self).serialize_field(field, text, author, tags)

# process = CrawlerProcess()

settings = get_project_settings()
settings.overrides['FEED_URI'] = 'quotes_7.csv'
settings.overrides['FEED_FORMAT'] = 'csv'

process = CrawlerProcess(settings)
process.crawl(ScrapeArticle)
process.start()


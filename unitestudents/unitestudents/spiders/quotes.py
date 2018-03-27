import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://www.unitestudents.com/',
            ]

    # Step 1
    def parse(self, response):
        for city in response.xpath('//select[@id="frm_homeSelect_city"]/option[not(contains(text(),"Select your city"))]/text()').extract(): # Select all cities listed in the select (exclude the "Select your city" option)
            yield scrapy.Request(response.urljoin("/"+city), callback=self.parse_citypage)

    # Step 2
    def parse_citypage(self, response):
        for url in response.xpath('//div[@class="property-header"]/h3/span/a/@href').extract(): #Select for each property the url
            yield scrapy.Request(response.urljoin(url), callback=self.parse_unitpage)

        # I could not find any pagination. Otherwise it would go here.

    # Step 3
    def parse_unitpage(self, response):
        unitTypes = response.xpath('//div[@class="room-type-block"]/h5/text()').extract() + response.xpath('//h4[@class="content__header"]/text()').extract()
        for unitType in unitTypes: # There can be multiple unit types so we yield an item for each unit type we can find.
            yield {
                'name': response.xpath('//h1/span/text()').extract_first(),
                'type': unitType,
                # 'price': response.xpath('XPATH GOES HERE'), # Could not find a price on the page
                # 'distance_beds': response.xpath('XPATH GOES HERE') # Could not find such info
            }

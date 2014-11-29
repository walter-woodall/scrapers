from scrapy.spider import CrawlSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Join, MapCompose

from walmart_scraper.items import WalmartScraperItem

class WalmartFoodSpider(CrawlSpider):
	name = "walmart_scraper"
	allowed_domains = ["walmart.com"]
	start_urls = ["http://www.walmart.com/cp/976759"]

	items_list_xpath = '//div[@class="js-tile tile-grid-unit"]'
	item_fields = {'title'	: './/a[@class="js-product-title"]/h3[@class="tile-heading"]/div',
					'image_url' : './/a[@class="js-product-image"]/img[@class="product-image"]/@src',
					'price' : './/div[@class="tile-price"]/div[@class="item-price-container"]/span[@class="price price-display"]|//div[@class="tile-price"]/div[@class="item-price-container"]/span[@class="price price-display price-not-available"]',
					'category' : '//nav[@id="breadcrumb-container"]/ol[@class="breadcrumb-list"]/li[@class="js-breadcrumb breadcrumb "][2]/a',
					'subcategory' : '//nav[@id="breadcrumb-container"]/ol[@class="breadcrumb-list"]/li[@class="js-breadcrumb breadcrumb active"]/a'}

	def parse(self, response):
        """
        Default callback used by Scrapy to process downloaded responses

        Testing contracts:
        @url http://www.livingsocial.com/cities/15-san-francisco
        @returns items 1
        @scrapes title link

        """
        selector = HtmlXPathSelector(response)

        # iterate over deals
        for item in selector.select(self.deals_list_xpath):
            loader = XPathItemLoader(WalmartScraperItem(), selector=item)

            # define processors
            loader.default_input_processor = MapCompose(unicode.strip)
            loader.default_output_processor = Join()

            # iterate over fields and add xpaths to the loader
            for field, xpath in self.item_fields.iteritems():
                loader.add_xpath(field, xpath)
            yield loader.load_item()
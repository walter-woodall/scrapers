__author__ = 'aymon'

import scrapy, re
from amznfrsh.items import GroceryItem
from scrapy.http import Request

class AmazonSpider(scrapy.Spider):
    name = "amzn"
    allowed_domains = ["fresh.amazon.com/"]
    start_urls = [
        "https://fresh.amazon.com/Gateway?browseZIP=20740&referer=Search%253Finput%253D%2526sort%253Dprice_low_to_high%2526browseNode%253D16310101%2526ref_%253Dgr_bb_s1%2526resultsPerPage%253D100"
    ]

    max_page = 286  #286 x 100 per page

    def start_requests(self):
            for i in range(self.max_page):
                yield Request('https://fresh.amazon.com/Gateway?browseZIP=20740&referer=Search%253Finput%253D%2526sort%253Dprice_low_to_high%2526pageNumber%253D{page}%2526browseNode%253D16310101%2526ref_%253Dgr_bb_s1%2526resultsPerPage%253D100'.format(page=i), callback=self.parse)

    def parse(self, response):
        for sel in response.xpath('//*[@id="searchResults"]/div[3]/div'):
            item = GroceryItem()
            try:
                title = sel.xpath('div/div[3]/div[3]/h4/input/@value').extract()[0]
                price = sel.xpath('div/div[3]/div[3]/div/span/text()').extract()
                if len(price) > 0:
                    m = re.search('\$\d+\.\d+', str(price[0]))
                    if m is not None:
                        price = m.group(0)

                url = sel.xpath('div/div[3]/div[3]/h4/a/@href').extract()[0]
                img = sel.xpath('div/div[3]/div[2]/div/a/img/@src').extract()[0]
                #print img
                print title, price, url
                item['name'] = title
                item['url'] = url
                item['price'] = price
                item['bigImage'] = img
                yield item
            except IndexError:
                print "poop"


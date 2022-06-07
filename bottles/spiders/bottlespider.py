import scrapy
from bottles.items import BottlesItem

class BottlespiderSpider(scrapy.Spider):
    name = 'bottlespider'
    allowed_domains = ['www.whiskyshop.com']
    start_urls = ['https://www.whiskyshop.com/exclusives','https://www.whiskyshop.com/single-malt-scotch-whisky/speyside']

    def parse(self, response):
        item = BottlesItem()
        for products in response.css('div.product-item-info'):

            item['name'] = response.css('div.product-item-link::text').get()
            item['price'] = response.css('span.price::text').get()
            item['link'] = response.css('a.product-item-link').get()

            yield item

        next_page = response.css('a.action.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

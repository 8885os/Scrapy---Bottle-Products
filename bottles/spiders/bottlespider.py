import scrapy
from bottles.items import BottlesItem
from scrapy.loader import ItemLoader

class BottlespiderSpider(scrapy.Spider):
    name = 'bottlespider'
    allowed_domains = ['www.whiskyshop.com']
    start_urls = ['https://www.whiskyshop.com/exclusives','https://www.whiskyshop.com/single-malt-scotch-whisky/speyside']

    def parse(self, response):
        
        for products in response.css('div.product-item-info'):
            l = ItemLoader(item = BottlesItem(), selector=products)
            l.add_css('name', 'a.product-item-link')
            l.add_css('price', 'span.price')
            l.add_css('link', 'a.product-item-link::attr(href)')

            yield l.load_item()

        next_page = response.css('a.action.next').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

# coding=utf-8
import scrapy
from ..items import BookItem
from scrapy.settings import default_settings
from scrapy.linkextractor import LinkExtractor


class BookSpider(scrapy.Spider):
    name='books'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        link_regulation = LinkExtractor(restrict_css='section')
        url_list = link_regulation.extract_links(response)
        if url_list:
            for link in url_list:
                url = link.url
                if 'page-' in url:
                    yield scrapy.Request(url, callback=self.parse)
                else:
                    yield  scrapy.Request(url,callback=self.parse_detail)

    def parse_detail(self, response):
        item = BookItem()
        item['name'] = name
        item['price'] = price
        yield item




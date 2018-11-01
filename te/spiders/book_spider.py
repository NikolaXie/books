# coding=utf-8
import scrapy
from ..items import BookItem
from scrapy.settings import default_settings
from scrapy.linkextractor import LinkExtractor
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from scrapy_redis.spiders import RedisSpider


class BookSpider(RedisSpider):
    name='books'
    # start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for book in response.css('article.product_pod'):
            name = book.xpath('./h3/a/@title').extract_first()
            price = book.css('p.price_color::text').extract_first()
            item = BookItem()
            item['name'] = name
            item['price'] = price
            yield item
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url,callback=self.parse)



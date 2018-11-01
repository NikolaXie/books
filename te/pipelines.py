# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
import pymongo
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ExchangeratePipeline(object):
    """
    汇率转换
    """
    rate = 8.34
    def process_item(self, item, spider):
        price = float(item['price'][1:]) * self.rate
        item['price'] = '￥%.2f' % price
        return item


class DuplicatesPipeline(object):
    """
     数据去重
    """
    def __init__(self):
        self.set = set()

    def process_item(self, itme, spider):
        if itme['name'] in self.set:
            raise DropItem
        self.set.add(itme['name'])
        return itme


class MongoSave(object):
    """
    将数据保存在mongodb中
    """
    MONGO_URL = 'mongodb://132.232.8.19:27017/'
    db_name = 'books'

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.MONGO_URL)
        self.db = self.client[self.db_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        collection.insert_one(dict(item))
        return item

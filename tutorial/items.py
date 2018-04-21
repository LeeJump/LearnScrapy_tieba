# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import MapCompose, Join
from scrapy.loader import ItemLoader


class postItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    replys = scrapy.Field()
    abstract = scrapy.Field(input_processor=lambda x: ''.join(x).replace('\n', '').strip())
    author = scrapy.Field()
    last_replyer = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                   insert into posts(replys, title, abstract, author,last_replyer)
                   VALUES (%s, %s, %s, %s,%s);
               """
        params = (
            self["replys"], self["title"], self["abstract"], self["author"], self["last_replyer"])
        return insert_sql, params

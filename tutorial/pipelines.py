# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql  # PYTHON中mysql库

'''
Python 中提供了 Twisted 框架来实现异步操作，该框架提供了一个连接池，通过连接池可以实现数据插入 MySQL 的异步化。
'''
from twisted.enterprise import adbapi


class MysqlTwistedPipline(object):
    def __init__(self, ):
        dbparms = dict(
            host='localhost',
            db='tieba',
            user='root',
            passwd='root',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        self.dbpool = adbapi.ConnectionPool("pymysql", **dbparms)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)
        return

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

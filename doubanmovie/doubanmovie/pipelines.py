# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from scrapy.conf import settings

class DoubanmoviePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(
            host = settings['MYSQL_HOST'],
            port = settings['MYSQL_PORT'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            db = settings['MYSQL_DB'],
            charset='utf8',
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        try:
            sql = "insert into douban250(name, actor, rating, info) values(%s,%s,%s,%s)"
            self.cursor.execute(sql, (item['name'], item['actor'], item['rating'], item['info']))
            self.conn.commit()
        except Exception as e:
            print(e)
        return item
    def close_spider(self, spider):
        self.conn.close()
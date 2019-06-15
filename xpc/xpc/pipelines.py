# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class MysqlPipeline(object):

    def __init__(self):
        self.conn = None
        self.cur = None

    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',
            db='xpc_1901',
            charset='utf8mb4'
        )
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        # "insert into `posts` (`pid`, `title`) values ('123', 'test')"
        #  insert into `copyrights` (pcid,pid,cid,roles) values ('123_456', '123', '456', '演员')
        #  on duplicate key update pcid='123_456', pid='123', cid='456', roles='演员2';
        keys, values = list(zip(*item.items()))
        sql = "insert into `%s` (%s) values (%s) on duplicate key update %s" % (
            item.table_name,
            ','.join(['`%s`' % k for k in keys]),
            ','.join(['%s'] * len(values)),
            ','.join("`{}`=%s".format(k) for k in keys)
        )
        self.cur.execute(sql, values * 2)
        self.conn.commit()
        print(self.cur._last_executed)
        return item

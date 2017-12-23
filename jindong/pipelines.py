# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class JindongPipeline(object):
    def __init__(self):
    	self.conn=pymysql.connect(host='127.0.0.1',user='root',passwd="123",db="jd",charset="utf8",use_unicode=False)

    def process_item(self, item, spider):
    	try:
    		names=item['name']
    		url=item['goodsurl']
    		price=item['price'].strip()
    		haop=item['haop'].strip()
    		sql="insert into jd(names,url,price,haop) values(%s,%s,%s,%s)"
    		self.cursor=self.conn.cursor()
    		self.cursor.execute(sql,(names,url,price,haop))
    		return item
    	except Exception as error:
    		log(error)

    def close_spider(self,spider):
    	self.conn.colse()
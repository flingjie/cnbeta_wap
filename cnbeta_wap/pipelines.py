# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import couchdb


class CnbetaWapPipeline(object):
    def __init__(self):
        server = couchdb.Server()
        try:
            self.db = server['cnbeta']
        except Exception as e:
            self.db = server.create('cnbeta')

    def process_item(self, item, spider):
        data = {
            'title': item['title'],
            'time': item['time'],
            'source': item['source'],
            'content': item['content']
        }
        map_fun = u'''
                    function(doc) {{
                     if(doc.title == "{}")
                        emit(doc.title, doc.time);
                     }}'''.format(item['title'])
        result = self.db.query(map_fun)
        if len(result) == 0:
            self.db.save(data)
        return item

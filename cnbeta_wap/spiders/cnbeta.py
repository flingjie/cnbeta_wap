# coding=utf8
from __future__ import absolute_import
import scrapy
from scrapy import log
from scrapy.conf import settings
from ..items import CnbetaWapItem


class CNBetaSpider(scrapy.Spider):
    name = "cnbeta"
    allowed_domains = ["m.cnbeta.com"]
    start_urls = [
        "http://m.cnbeta.com/wap/index.htm"
    ]

    def __init__(self):
        self.cur_page = 1

    def parse(self, response):
        items = response.selector.xpath('//div[@class="list"]/a/@href').extract()
        for i in items:
            item_url = "http://m.cnbeta.com{}".format(i)
            yield scrapy.Request(url=item_url, callback=self.parse_item)

        self.cur_page += 1
        if self.cur_page <= settings["MAX_PAGE"]:
            url = "http://m.cnbeta.com/wap/index.htm?page={}".format(self.cur_page)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_item(self, response):
        try:
            item = CnbetaWapItem()
            item['title'] = response.selector.xpath('//div[@class="title"]/b/text()').extract()[0]
            item['time'] = response.selector.xpath('//div[@class="time"]/span/text()').extract()[0][5:]
            item['source'] = response.selector.xpath('//div[@class="time"]/span/text()').extract()[1]
            item['content'] = response.selector.xpath('//div[@class="content"]').extract()[0]
            yield item
        except Exception as e:
            log.msg(str(e), level=log.ERROR)
            import traceback
            traceback.print_exc()




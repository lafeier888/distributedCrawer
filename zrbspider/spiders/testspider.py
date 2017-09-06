# -*- coding: utf-8 -*-
import scrapy


class TestspiderSpider(scrapy.Spider):
    name = "testspider"
    allowed_domains = ["dangdang.com"]
    start_urls = ['http://dangdang.com/']

    def parse(self, response):
        pass

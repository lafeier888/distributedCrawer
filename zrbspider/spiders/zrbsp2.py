# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request, HtmlResponse

import json
import os
import sys
class Zrbsp2Spider(CrawlSpider):
    name = 'zrbsp2'
    allowed_domains = ['jd.com']
    start_urls = ['http://www.jd.com/']

    rules = (
        Rule(LinkExtractor(allow=r'shouji'), callback='parse_item', follow=True),
    )

    global splashurl;
    splashurl = "http://211.159.180.183:8050/render.html";

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
    def make_requests_from_url(self, url):
        url = splashurl + "?url=" + url;
        # body = json.dumps({"url": url, "wait": 5, 'images': 0, 'allowed_content_types': 'text/html; charset=utf-8'})
        # headers = {'Content-Type': 'application/json'}
        return Request(url,dont_filter=True)
    def parse_start_url(self, response):
        save_name = response.selector.xpath("//title/text()").extract()
        # save_name_u = save_name[0].encode('utf-8')
        with open(save_name[0],'wb') as ff:
            ff.write(response.body)
        # if save_name[0]:
        #     file_path = self.webpath + "/" + self.url_domain+ "/" + save_name[0] + '.html'
        #     file_path = file_path.encode('utf-8')
        #     item=ZrbspiderItem()
        #     item['title']=save_name[0]+'.html'
        #     yield item
        #     with open(file_path, "wb") as save_html:
        #         save_html.write(response.body)
        pass
    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i

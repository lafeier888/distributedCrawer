# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from scrapy.http import Request, HtmlResponse
from scrapy.selector import Selector
import json


class zrbspiders(Spider):
    name = 'zrbspiders'
    start_urls = [
        'https://www.taobao.com'
    ]
    global splashurl;
    splashurl = "http://211.159.180.183:8050/render.html";  # splash 服务器地址

    # 此处是重父类方法，并使把url传给splash解析
    # def make_requests_from_url(self, url):
    #     global splashurl;
    #     url = splashurl + "?url=" + url;
    #     body = json.dumps({"url": url, "wait": 50, 'images': 0, 'allowed_content_types': 'text/html; charset=utf-8'})
    #     headers = {'Content-Type': 'application/json'}
    #     return Request(url, body=body, headers=headers, dont_filter=True)

    def parse(self, response):
        print "############" + response._url
        # print response.body
        fo = open("jde222e.html", "wb")
        fo.write(response.body);  # 写入文件
        fo.close();
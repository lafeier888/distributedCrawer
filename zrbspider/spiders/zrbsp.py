# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request, HtmlResponse
from scrapy import log
log.msg("This is a warning", level=log.CRITICAL)
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ZrbspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title=scrapy.Field()
    pass

class ZrbspSpider(CrawlSpider):
    def __init__(self, start_url='https://www.taobao.com'):
        self.webpath = '/var/www/zrbspider/zrbspider/web/'
        self.start_urls = []
        self.allowed_domains=[]
        self.ru=[]
        self.urldomain=[]
        # self.rulepath = os.path.abspath('.') + "/rules.json"
        # with open("/var/www/zrbspider/zrbspider/spiders/rules.json", "r") as fi:
        #     fii=fi.read()
        #     file_rule = json.load(fi)
        # print rulepath
        # print webpath
        with open("/var/www/zrbspider/zrbspider/spiders/rules.json", "r") as fi:
            file_rule = json.load(fi)
        print start_url
        self.start_urls.append(start_url)
        print self.start_urls

        urlstr=start_url.split(".")
        self.url_domain = urlstr[1]
        # self.allowed_domains.append(urlstr[1]+'.com')
        # self.allowed_domains.append(urlstr[1]+'cn')
        # self.allowed_domains.append(urlstr[1] + 'net')
        if not os.path.exists(self.webpath+'/' +urlstr[1]):
            os.mkdir(self.webpath + '/'+urlstr[1])
        if file_rule[urlstr[1]]:
            for rul in file_rule[urlstr[1]]:
                thisrule=Rule(LinkExtractor(allow=rul['allow'], deny=rul['deny']),callback=rul['callback'], follow =rul['follow'])
                self.ru.append(thisrule)
        self.rules = tuple(self.ru)
        super(ZrbspSpider,self).__init__()
    name = 'zrbsp'
    # allowed_domains = ['taobao.com']
    # start_urls = ['https://www.taobao.com/']
    # link = LinkExtractor(allow=('/shouji'))
    # rules = (
    #     Rule(link,callback='parse_item ')
    # )

    global splashurl;
    splashurl = "http://211.159.180.183:8050/render.html";

    def start_requests(self):
        for url in self.start_urls:
            yield self.make_requests_from_url(url)
    def make_requests_from_url(self, url):
        url = splashurl + "?url=" + url;
        # body = json.dumps({"url": url, "wait": 5, 'images': 0, 'allowed_content_types': 'text/html; charset=utf-8'})
        # headers = {'Content-Type': 'application/json'}
        return Request(url,  dont_filter=True)
    def parse_start_url(self, response):
        save_name = response.selector.xpath("//title/text()").extract()
        print save_name[0].encode('GBK')
        if save_name[0]:
            file_path = self.webpath + self.url_domain+ "/" + save_name[0] + '.html'
            file_path = file_path.encode('utf-8')
            item=ZrbspiderItem()
            item['title']=save_name[0]+'.html'
            yield item
            with open(file_path, "wb") as save_html:
                save_html.write(response.body)
        pass
    def parse_item(self, response):
        save_name = response.selector.xpath("//title/text()").extract()
        print save_name[0].encode('utf-8')
        if save_name[0]:
            item = ZrbspiderItem()
            item['title'] = save_name[0]+'.html'
            yield item
            file_path = self.webpath +  self.url_domain + "/" + save_name[0]+ '.html'
            file_path = file_path.decode('utf-8').encode('utf-8')
            print file_path
            with open(file_path, "wb") as save_html:
                save_html.write(response.body)
        pass




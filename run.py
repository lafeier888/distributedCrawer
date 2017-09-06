# -*- coding: utf-8 -*-
import multiprocessing
import redis
import time
import os
from scrapy.cmdline import execute

class serverrun():
    def __init__(self,start,num=1):
        # os.chdir('/var/www/zrbspider/zrbspider/')
        self.num = num
        self.start = start
        self.a = []
        # self.r=redis.Redis(host='211.159.180.183', port=6379,db=1)
    def runspider(self):
        execute(['scrapy', 'crawl', 'zrbsp', '-a', "start_url=" + self.start])
    def run(self):
        for i in range(int(self.num)):
            p = multiprocessing.Process(target=self.runspider)
            p.start()
            print p.pid
            print p.name
            self.r.rpush('process', p.pid)
    def test(self):
        return 789456



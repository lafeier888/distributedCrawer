# -*- coding:utf-8 -*-
import web
import json
import redis
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
urls = (
    "/","test",
)
test = web.application(urls, globals())
redisurl = '211.159.180.183'
localhosturl = '127.0.0.1'
redis_passwd = 'tian123'

class test:
    def GET(self):
        # web.header('Access-Control-Allow-Origin', '*')
        return '456'


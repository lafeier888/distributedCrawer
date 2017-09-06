# -*- coding:utf-8 -*-
import web
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
urls = (
    "/spider","spider",
    "/wconfig","wconfig"
)

REDIS_SERVER_URL = '127.0.0.1'
REDIS_SERVER_PASSWD = 'tian123'
config_app = web.application(urls, globals())
class spider:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        with open('/var/www/zrbspider/zrbspider/spiders/rules.json','r') as f:
            data = json.load(f)
        return json.dumps(data)
class wconfig:
    def POST(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        x = web.data()
        with open('/var/www/zrbspider/zrbspider/spiders/rules.json','wb') as f:
            f.write(x)
        return x


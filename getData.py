# -*- coding:utf-8 -*-
import web
import sys
import redis
import json
reload(sys)
sys.setdefaultencoding('utf-8')
urls = (
    '/request', 'request',
  "/items", "items",
    "/getdata","getdata"
)
redisurl = '211.159.180.183'
localhosturl = '127.0.0.1'
redis_passwd = 'tian123'
getData_app = web.application(urls, globals())
class request:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        x = web.input()
        if x.has_key('url_domain'):
            r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=redis_passwd)
            requests=r.scard(x['url_domain']+':dupefilter')
            return requests
        else:
            r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=redis_passwd)
            if web.cookies().get('url_domain'):
                requests = r.scard(web.cookies().get('url_domain') + ':dupefilter')
                return requests
            else:
                with open('/var/www/zrbspider/zrbspider/url.json') as f:
                    url_json = json.load(f)
                url_domain = url_json['urldomain']
                web.setcookie('url_domain',url_domain, 300)
                requests = r.llen(url_domain + ':dupefilter')
                return requests

class items:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        x = web.input()
        if x.has_key('url_domain'):
            url_domain= x['url_domain']
            r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=redis_passwd)
            items = r.llen(url_domain+':items')
            return items
        else:
            r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=redis_passwd)
            if web.cookies().get('url_domain'):
                items = r.scard(web.cookies().get('url_domain') + ':items')
                return items
            else:
                with open('/var/www/zrbspider/zrbspider/url.json') as f:
                    url_json = json.load(f)
                url_domain = url_json['urldomain']
                web.setcookie('url_domain', url_domain, 300)
                items = r.scard(url_domain + ':items')
                return items

        # return json.dumps(data)
#获取数据
class getdata:
    def GET(self):
        p = web.input()
        web.header('Access-Control-Allow-Origin','*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        page = int(p.page)
        size =20
        start = page*int(size)
        end = (page+1)*size
        r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=redis_passwd)
        if p.has_key('url_domain'):
            url_domain = p['url_domain']
            item = url_domain+':items'
            data=r.lrange(item,start=start,end=end)
            datalength = r.llen(item)
            ajaxdata=[]
            jsondata = {}
            if datalength:
                if data:
                    for i in data:
                        f=json.loads(i)
                        s=f['title']
                        ajaxdata.append(s.encode('utf-8'))
                    jsondata['data'] =ajaxdata
                    return json.dumps(jsondata,ensure_ascii=False)
                else:
                    return 22
            else:
                return 11
        else:
            return '{"msg":"没有传递url_domain参数"}'
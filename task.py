# -*- coding:utf-8 -*-
import web
import json
import redis
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
urls = (
    "/task","task",
    '/tasktest','test'
)
redisurl = '211.159.180.183'
localhosturl = '127.0.0.1'
redis_passwd = 'tian123'
task_app = web.application(urls, globals())
class task:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=redis_passwd)
        task_data = r.lrange('task',start=0,end=-1)
        task_json = {}
        # return type(task_data)
        # return json.loads(task_data)
        task_json['data']= task_data
        return json.dumps(task_json,ensure_ascii=False)
class test:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        r = redis.Redis(host='127.0.0.1', port=6379, db=0,password=redis_passwd)
        task_data = r.lrange('task', start=0, end=-1)
        for i in task_data:
            eval(i)
            return i

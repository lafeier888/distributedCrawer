# -*- coding:utf-8 -*-
import os
import web
import multiprocessing
import zipfile
import sets
import redis
import random

# import run
import time
import json
import re
from scrapy.cmdline import execute
import sys
import urllib2
import chardet

reload(sys)
sys.setdefaultencoding('utf-8')
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
sys.path.append('/var/www/zrbspider/zrbspider/')
os.chdir(abspath)

from lafeier.AutoStruct import *
import config

# import test
import task
# import struct
import train
import getData
# import run
# sys.path.append('./var/www/zrbspider/zrbspider/')
urls = (
  '/', 'index',
    '/getdata',getData.getData_app,
    '/config',config.config_app,
    # '/struct',struct.struct_app,
    '/train',train.train_app,
    '/task',task.task_app,
    '/force','force_stop',
    # '/test',test.test,
    '/structdata','structdata',
    '/structd','structd',
    '/run', 'run',
     '/stop', 'stop',
    '/gettpl','gettpl',
    '/pause','pause',
    '/yema','yema'
)
redisurl = '211.159.180.183'
localhosturl = '127.0.0.1'
redis_passwd = 'tian123'
# web.config.debug = True

path = '/var/www/zrbspider/zrbspider/'
application = web.application(urls, globals(),True).wsgifunc()



#主界面
class index:
    def GET(self,):
        return web.redirect('http://zrb.gotohard.cn/static/')
#获取请求数
class load:
    def GET(self):
        # f = os.getcwd()
        f = open('/var/www/zrbspider/zrbspider/jiegouhua/jd.txt','r')
        return f.read(), '<hr>', sys.path, '<hr>',abspath

#启动爬虫
class run:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        i = web.input()
        num = i.num
        start = i.start

        if not i.has_key('url_domain'):
            #g如果没有传入url_domain
            zz=r'((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?'
            zz_url_start = re.search(zz,start)

            #判断是否是网址
            if zz_url_start:
                domain = start.split('.')
                url_do ={}
                if len(domain)==2:
                    start_url = zz_url_start.group(1)+'www.'+zz_url_start.group(3)
                    redis_domain = start_url.split('.')
                    domain = redis_domain[1]
                    return self.isnew_run(domain=domain, start=start_url, num=num,)

                else:
                    domain = domain[1]
                    return self.isnew_run(domain=domain, start=start, num=num)
            else:
                return '传入的不是网址！'
        else:
            return 258369
            #如果传入url_domain
            domain = i['url_domain']
            self.isnew_run(domain=domain,start=start,num=num,isnew=False)

    def isnew_run(self,domain,start,num,isnew=True):
        r = redis.Redis(localhosturl, port=6379, db=0, password=redis_passwd)
        with open('/var/www/zrbspider/zrbspider/url.json', 'w') as f:
            url_do = {}
            url_do['urldomain'] = domain
            f.write(json.dumps(url_do))
        if isnew:
            task = r.lrange('task', start=0, end=-1)
            if task:
                for i in task:
                    i = eval(i)
                    if i['taskName'] == domain:
                        run3 = serverrun(num=num, start=start, domain=domain, isnew=False)
                        re_data = {}
                        re_data['path'] = '/var/www/zrbspdier/zrbspide/web/' + domain
                        re_data['taskname'] = domain
                        re_data['status'] = run3.run()
                        return json.dumps(re_data)
                    else:
                        run4 = serverrun(num=num, start=start, domain=domain)
                        re_data = {}
                        re_data['path'] = '/var/www/zrbspdier/zrbspide/web/' + domain
                        re_data['taskname'] = domain
                        re_data['status'] = run4.run()
                        # return 4567
                        return json.dumps(re_data)
            else:
                run1 = serverrun(num=num, start=start, domain=domain)
                re_data = {}
                re_data['path'] = '/var/www/zrbspdier/zrbspide/web/' + domain
                re_data['taskname'] = domain
                re_data['status'] = run1.run()
                return json.dumps(re_data)
        else:
            run2 = serverrun(num=num, start=start, domain=domain, isnew=False)
            re_data = {}
            re_data['path'] = '/var/www/zrbspdier/zrbspide/web/' + domain
            re_data['taskname'] = domain
            run2.run()
            return json.dumps(re_data)


class pause:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        x = web.input()
        url_domain = x['url_domain']
        r = redis.Redis(localhosturl, port=6379, db=0,password=redis_passwd)
        taskdata = r.lrange('task',start=0,end=-1)
        r.delete('task')
        for i in taskdata:
            i = eval(i)
            if i['taskName']==url_domain:
                a = i['pid']
                for t in a:
                    os.system('kill -s 9 ' + t)
                    return t
                i['pid']=[]
                i['taskStatus'] = 1
                i['taskNum'] =0
            data = json.dumps(i)
            r.lpush('task',data)
        return 666666
class force_stop:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        r = redis.Redis(localhosturl, port=6379, db=0, password=redis_passwd)
        jincheng = r.llen('process')
        if jincheng:
            for i in range(jincheng):
                n = r.rpop('process')
                os.system('kill -s 9 ' + n)
class stop:
    def GET(self):
        x = web.input()
        url_domain = x['url_domain']
        r = redis.Redis(localhosturl, port=6379, db=0, password=redis_passwd)
        taskdata = r.lrange('task', start=0, end=-1)
        r.delete('task')
        for i in taskdata:
            i = eval(i)
            if i['taskName'] == url_domain:
                a = i['pid']
                for t in a:
                    os.system('kill -s 9 ' + str(t))
                    # n=r.rpop('process')
                    # return t
                i['pid'] = []
                i['taskStatus'] = 0
                i['taskNum'] = 0
            data = json.dumps(i)
            r.lpush('task', data)
        r.delete(url_domain + ':dupefilter', url_domain + ':requests')
        return 666
class serverrun():
    def __init__(self, start,domain, num=1,isnew=True):
        os.chdir('/var/www/zrbspider/zrbspider/')
        self.num = num
        self.domain =domain
        self.start = start
        self.a = []
        self.r=redis.Redis(localhosturl, port=6379, db=0,password=redis_passwd)
        self.isnew = isnew
    def runspider(self):
        execute(['scrapy', 'crawl', 'zrbsp', '-a', "start_url=" + self.start])
    def run(self):
        pid_n = []
        for i in range(int(self.num)):
            p = multiprocessing.Process(target=self.runspider)
            p.start()
            pid_n.append(p.pid)
            self.r.rpush('process', p.pid)
        if not self.isnew:
            # return 'bushi'
            taskdata = self.r.lrange('task', start=0, end=-1)
            self.r.delete('task')
            for i in taskdata:
                i = eval(i)
                if i['taskName']==self.domain:
                    if i['taskNum']:
                        num = i['taskNum']
                        i['taskNum']=int(self.num)+int(num)
                    else:
                        i['taskNum'] = self.num
                    i['taskStatus']=2
                    i['pid']=i['pid']+pid_n
                data = json.dumps(i)
                self.r.lpush('task',data)
            return 666
        else:
            # return 'shi'
            taskData = {}
            taskData['taskUrl'] = self.start
            taskData['taskName'] = self.domain
            taskData['taskNum'] = self.num
            taskData['taskStatus'] = 2

            taskData['pid'] = pid_n
            data = json.dumps(taskData)
            self.r.lpush('task',data)
            return 6666
class structd:
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        return """<html><head></head><body>
    <form method="POST" enctype="multipart/form-data" action="http://zrb.gotohard.cn/struct">
    <input type="file" name="myfile" />
    <br/>
    <input type="text" name="select"/>
    <input type="submit" />
    </form>
    </body></html>"""
    def POST(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        reload(sys)
        sys.setdefaultencoding('utf-8')
        # web.header("Content-Type", "text/html; charset=utf-8")
        x = web.input(myfile={})
        d = web.input()
        # j=web.data()
        # da=json.loads(d)
        filedir = '/var/www/zrbspider/zrbspider/jiegouhua/'  # change this to the directory you want to store the file in.
        # return filedir
        if 'myfile' in x:  # to check if the file-object is created
            filepath = x['myfile'].filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
            filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
            filename = filename.decode('utf-8')
            ishtml = re.search('html',filename)
            if ishtml:
                #单个文件结构化
                filename = filename.decode('utf-8')
                htmlpath = filedir +'structhtml/'+ filename.encode('utf-8')
                fout = open(htmlpath, 'wb')  # creates the file where the uploaded file should be stored
                fout.write(x['myfile'].file.read())  # writes the uploaded file to the newly created file.
                fout.close()
                tplname = x['select']
                # 模板名字，用来存数据库
                tplpath = '/var/www/zrbspider/zrbspider/jiegouhua/tpl/' + tplname

                try:
                    data = struct(htmlFilePath=htmlpath, tplFilePath=tplpath,encoding = 'utf-8')
                except (UnicodeDecodeError, UnicodeEncodeError):
                    try:
                        data = struct(htmlFilePath=htmlpath, tplFilePath=tplpath,encoding='gb18030')

                    except (UnicodeDecodeError, UnicodeEncodeError):
                        try:
                            data = struct(htmlFilePath=htmlpath, tplFilePath=tplpath,encoding='gbk')
                        except (UnicodeDecodeError, UnicodeEncodeError):
                            data = struct(htmlFilePath=htmlpath, tplFilePath=tplpath,encoding='gb2312')
                with open('./bugg.txt','a') as f:
                    f.write(str(data))
                r = redis.Redis(localhosturl, port=6379, db=0, password=redis_passwd)
                r.lpush(tplname, json.dumps(data['data']))
                pass
            else:
                #网页压缩包结构化
                filename = filename.decode('utf-8')
                zippath = filedir+'htmlzip/'+filename.encode('utf-8')
                # return filepath, filename, chardet.detect(filepath),filepath.decode('utf-8'),chardet.detect(filename),filename.decode('utf-8')
                # return zippath
                fout = open(zippath, 'wb')  # creates the file where the uploaded file should be stored
                fout.write(x['myfile'].file.read())  # writes the uploaded file to the newly created file.
                fout.close()  # closes the file, upload complete.
                # return "filename: %s\n " % (x['myfile'].filename)
                tplname=x['select']
                #模板名字，用来存数据库

                #构造启解压后的文件目录
                zip_un_html = filename.split('.')
                savePath = filedir+'htmlzip/' + zip_un_html[0]
                savePath = savePath.encode('utf-8')
                tplpath='/var/www/zrbspider/zrbspider/jiegouhua/tpl/'+tplname
                dictor = {}
                # return zippath.decode('utf-8'), savePath.decode('utf-8'), tplpath.decode('utf-8'), rtplname[0],
                try:

                    alldata = structure(zipFileName=zippath, savePath=savePath, tpl=tplpath,
                                     tplname=tplname, encoding='utf-8')
                    dictor['data1']=alldata
                except (UnicodeDecodeError, UnicodeEncodeError):
                    try:

                        alldata = structure(zipFileName=zippath, savePath=savePath, tpl=tplpath,
                                         tplname=tplname, encoding='GB18030')

                        dictor['data2'] = alldata
                    except (UnicodeDecodeError, UnicodeEncodeError):
                        try:
                            alldata = structure(zipFileName=zippath, savePath=savePath, tpl=tplpath,
                                             tplname=tplname, encoding='GB2312')

                            dictor['data3'] = alldata
                        except (UnicodeDecodeError, UnicodeEncodeError):
                            alldata = structure(zipFileName=zippath, savePath=savePath, tpl=tplpath,
                                             tplname=tplname, encoding='GBK')
                            dictor['data4'] = alldata
                dirnum = lookThrough(savePath)
                dictor['dirnum'] = dirnum
                return dictor
        else:
            return 111
class structtest:
    def GET(self):
        x = web.input()
        tpl = x.tpl
        # html = x.html
        tplpath = '/var/www/zrbspider/zrbspider/jiegouhua/tpl/'+tpl
        htmlpath = '/var/www/zrbspider/zrbspider/jiegouhua/structhtml/'+html
        data = struct(htmlFilePath=htmlpath, tplFilePath=tplpath)
        return data

class yema:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        x = web.input()
        tplname = x['tplname']
        r = redis.Redis(localhosturl, port=6379, db=0, password=redis_passwd)
        num = r.llen(tplname)
        return num
        # return random.randint(0,99)
class AISpider:
    # 从本地文件训练
    # 参数：
    # [
    # 	{
    # 		"filename":"文件名",
    # 		"data":{
    # 			"字段名":值,
    # 			"字段名":值
    # 		}
    # 	}
    # 	……多个
    # ]
    @classmethod
    def trainFromLocalFiles(cls, items, tplName,saveFilename="", encoding='utf-8',cnTplName=""):
        s = Scraper()
        for item in items:
            file = open(item["filename"])
            content = file.read()
            page = HtmlPage(body=unicode(content.decode(encoding)), encoding=encoding)
            s.train_from_htmlpage(page, item["data"])
        if (saveFilename != ""):
            file = open(saveFilename, "wb")
            s.tofile(file)
            dic = {}
            dic['cnTplName'] = cnTplName
            dic['tplname'] = tplName
            r = redis.Redis(localhosturl, port=6379, db=0, password=redis_passwd)
            r.lpush('tplname', dic)
        return s

    # 从网址训练
    # 参数
    # [
    # 	{
    # 		"url":"网址",
    # 		"data":{
    # 			"字段名":值,
    # 			"字段名":值
    # 		}
    # 	}
    # 	……多个
    # ]
    @classmethod
    def trainFromUrls(cls, items, saveFilename="", encoding='utf-8'):
        s = Scraper()
        for item in items:
            s.train(item["url"], item["data"], encoding=encoding)
        if (saveFilename != ""):
            file = open(saveFilename, "wb")
            s.tofile(file)
        return s

    # 从以存在的模板获取一个Scrapely实例
    # 参数：文件名[必须]
    @classmethod
    def getScrapelyFromTpl(cls, filename):
        file = open(filename, "rb")
        return Scraper.fromfile(file)

    # 将本地网页转成Page对象
    @classmethod
    def fileToPage(csl, filename, encoding='utf-8'):
        file = open(filename)
        content = file.read()
        return HtmlPage(body=unicode(content.decode(encoding)), encoding=encoding)

#获取模板列表
class gettpl:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        r = redis.Redis(localhosturl, port=6379, db=0, password=redis_passwd)
        tpldata = r.lrange('tpl',0,-1)
        b = {}
        a = []
        for i in tpldata:
            o = eval(i)
            a.append(o)
        b['data'] = a
        return json.dumps(b,ensure_ascii=False)

class structdata:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        r = redis.Redis(localhosturl, port=6379, db=0, password=redis_passwd)
        i = web.input()
        tplname = i['tplname']
        page = i['page']
        num = 2
        start = int(num)*int(page)
        end = int(num)*(int(page)+1)
        data = r.lrange(tplname, start=start, end=end)
        datalenth = r.llen(tplname)
        if datalenth:
            dic = {}
            li = []
            for i in data:
                da = eval(i)
                li.append(da)
            dic['data']=li
            if dic['data']:
                return json.dumps(dic,ensure_ascii=False)
            else:
                if num*page>datalenth:
                    return 22
        else:
            return 11
        # 结构化

def structure(zipFileName, savePath, tpl, tplname, encoding='utf-8'):
    # 解压
    zipExtract(zipFileName, savePath, encoding=encoding)
    # 遍历文件
    alldata = []
    for url in lookThrough(savePath):
        try:
            data = struct(htmlFilePath=url, tplFilePath=tpl,encoding =encoding)
        except :
            with open('/var/www/zrbspider/buuug.txt','a') as f:
                f.write(str(data))
            continue
        r = redis.Redis(localhosturl, port=6379, db=0, password=redis_passwd)
        r.lpush(tplname, json.dumps(data['data']))
        alldata.append(data['data'])
    return alldata
    pass

# 解压函数
def zipExtract(filename, savePath,encoding ='utf-8'):
    file = zipfile.ZipFile(filename, "r")
    for name in file.namelist():
        utf8name = name
        dirname = savePath + '/' + os.path.dirname(utf8name)
        try:
            if not os.path.exists(dirname) and dirname != "":
                os.makedirs(dirname)
        except (UnicodeDecodeError, UnicodeEncodeError):
            try:
                dirname = dirname.decode('GBK').encode('utf-8')
                if not os.path.exists(dirname) and dirname != "":
                    os.makedirs(dirname)
            except (UnicodeDecodeError, UnicodeEncodeError):
                try:
                    dirname = dirname.decode('GB18030').encode('utf-8')
                    if not os.path.exists(dirname) and dirname != "":
                        os.makedirs(dirname)
                except (UnicodeDecodeError, UnicodeEncodeError):
                    dirname = dirname.decode('GBK2312').encode('utf-8')
                    if not os.path.exists(dirname) and dirname != "":
                        os.makedirs(dirname)
        data = file.read(name)
        dirname_encoding = getStrCoding(utf8name)
        utf8name = utf8name.decode(dirname_encoding).encode('utf-8')
        # utf8name = re.sub(r'\\\\',r'\\',utf8name)
        # b = utf8name.decode("string_escape")
        savedir = savePath + '/' + utf8name
        with open('/var/www/zrbspider/test.txt','w')as f:
            f.write(savedir)
        if not os.path.exists(os.path.dirname(os.path.abspath(savedir))):
            os.makedirs(os.path.dirname(os.path.abspath(savedir)))
        if not os.path.exists(savedir):
            fo = open(savedir, "w")
            fo.write(data)
            fo.close

    file.close()
    pass

# 遍历目录函数（去除目录，只保留文件）
def lookThrough(rootDir, dirs=set()):
    for lists in os.listdir(rootDir):
        path = os.path.join(rootDir, lists)
        if os.path.isdir(path):
            lookThrough(path)
        else:
            dirs.add(path)
    return list(dirs)

#检测编码
def getStrCoding(str):
    def getCoding(str):
        try:
            coding = codingList.pop()
            str.decode(coding)
            return coding
        except:
            return getCoding(str)
    codingList = ['gb18030', 'gbk','gb2312', 'utf-8']
    return getCoding(str)


# 调用事例
# print structure("自动化抽取-京东网页集合.zip","lafeier")
# autoSelectTpl("/home/python/Desktop/web/京东/12133.html")



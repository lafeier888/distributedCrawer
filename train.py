# -*- coding:utf-8 -*-
import web
import os
import json
import re
import requests
import time
import urllib2
import redis
from urllib2 import Request, urlopen, URLError, HTTPError
from lafeier.AutoStruct import *
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
urls = (
    '/', 'htmltrain',
  "/totrain", "totrain",
    "/fuzhi","fuzhi"
)
redisurl = '211.159.180.183'
localhosturl = '127.0.0.1'
redis_passwd = 'tian123'
train_app = web.application(urls, globals())
class test:
    def GET(self):
        x = web.input()
        return 0

class htmltrain:
    def GET(self):
        x = web.input()
        # web.header("Content-Type", "text/html; charset=utf-8")
        url = x['url']
        zz = r'((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,4})*(/[a-zA-Z0-9\&%_\./-~-]*)?'
        zz_url = re.search(zz, url)
        # url = 'https://item.taobao.com/item.htm?spm=a310p.7395725.1998460392.1.ffca6c0RPkCO6&id=549869514793'
        # renderurl = 'http://zrb.gotohard.cn:8050/render.html?url='+ url
        # headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        aaa = []
        if zz_url:
            iscsdn = re.search('csdn',url)
            iszhihu = re.search('zhihu',url)
            iscnblogs = re.search('cnblogs',url)
            if iscsdn or iszhihu or iscnblogs:
                try:
                    r = urllib2.urlopen(url)
                except HTTPError, e:
                    return 111
                a = url.split('/')
                host_url = a[0]+'//'+a[2]
                soup = BeautifulSoup(r.read(), 'html.parser')
                for i in soup.select('link'):
                    orgin_url = i['href']
                    a = re.search('//',orgin_url)
                    if a:
                        href = orgin_url
                    else:
                        href = host_url+orgin_url
                    i['href'] = 'http://zrb.gotohard.cn/train/fuzhi?url='+href+'&origin_url='+url
                for i in soup.select('img'):
                    orgin_url = i['src']
                    a = re.search('//',orgin_url)
                    if a:
                        href = orgin_url
                    else:
                        href = host_url+orgin_url
                    i['src'] = 'http://zrb.gotohard.cn/train/fuzhi?url='+href+'&origin_url='+url
                # for i in soup.select('script'):
                #     keys = i.attrs
                #     if keys.has_key('src'):
                #         orgin_url = i['src']
                #         a = re.search('//',orgin_url)
                #         if a:
                #             href = orgin_url
                #         else:
                #             href = host_url+orgin_url
                #         i['src'] = 'http://zrb.gotohard.cn/train/fuzhi?url='+href+'&origin_url='+url
                return soup.prettify()
            else:
                try:
                    r = urllib2.urlopen(url)
                except HTTPError,e:
                    return '网页找不到,错误代码404，2秒之后刷新页面！'
                return r.read()
        else:
            return '网页找不到,错误代码404，2秒之后刷新页面！'
        # a = url.split('/')
        # host_url = a[0]+'//'+a[2]
        # soup = BeautifulSoup(r.read(), 'html.parser')
        # for i in soup.select('link'):
        #     orgin_url = i['href']
        #     a = re.search('//',orgin_url)
        #     if a:
        #         href = orgin_url
        #     else:
        #         href = host_url+orgin_url
        #     i['href'] = 'http://zrb.gotohard.cn/train/fuzhi?url='+href+'&origin_url='+url

        # return r.text
        # return r.status_code,784548484
        # htmlname = str(int(time.time())) + '.html'
        # soup = BeautifulSoup(reponse.read())
        # with open(filedir+htmlname, 'wb') as f:
        #     f.write(reponse.read().decode('GBK').encode('utf-8'))
        #     return 'http://zrb.gotohard.cn/jiegouhua/'+htmlname
        # return os.getcwd(),os.path.dirname(__file__),666
    def POST(self):
        web.header('Access-Control-Allow-Origin', '*')
        # web.header("Content-Type", "Application/json; charset=utf-8")
        # return 'http://zrb.gotohard.cn/train/?url=https://www.zhihu.com/people/ma-shi-zhen/activities'
        info = {}
        web.header("Content-Type", "text/html; charset=utf-8")
        x = web.input(htmlfile={})
        j=web.data()
        items = {}
        dirname = os.path.dirname(__file__)
        filedir =dirname+ '/zrbspider/jiegouhua/trainhtml/'
        if not x['htmlfile']=={}:
            #文件名处理
            filepath = x['htmlfile'].filename.replace('\\', '/')
            filename = filepath.split('/')[-1]
            htmlpath = filedir + filename
            fout = open(htmlpath, 'wb')
            htmldata = x['htmlfile'].file.read()
            fout.write(htmldata)
            fout.close()
            return 'http://zrb.gotohard.cn/jiegouhua/'+filename
            #返回值
            # info['path'] = htmlpath
            # info['status'] = 666
            # info['value'] = x['itemdata']
            # # 组合参数
            # data = {}
            # args = []
            # items['filename'] = htmlpath
            # value = json.loads(info['value'])
            # items['data'] = value['item']
            # # return aaa['item'], type(info['value'])
            # tplname = value['tplName']
            # cnTplName = value['cnTplName']
            # tplpath = path+'jiegouhua/tpl/'+tplname
            # args.append(items)
            # with open('./train.txt','wb') as tra:
            #     tra.write(str(args)+cnTplName+tplname+tplpath)
            # try:
            #     AISpider.trainFromLocalFiles(items=args, tplName=tplname, saveFilename=tplpath, cnTplName=cnTplName,encoding='utf-8')
            # except UnicodeDecodeError:
            #     try:
            #         AISpider.trainFromLocalFiles(items=args, tplName=tplname, saveFilename=tplpath, cnTplName=cnTplName,
            #                                      encoding='GB18030')
            #     except UnicodeDecodeError:
            #         try:
            #             AISpider.trainFromLocalFiles(items=args, tplName=tplname, saveFilename=tplpath, cnTplName=cnTplName,
            #                                      encoding='GB2312')
            #         except UnicodeDecodeError:
            #             try:
            #                 AISpider.trainFromLocalFiles(items=args, tplName=tplname, saveFilename=tplpath,
            #                                              cnTplName=cnTplName,
            #                                              encoding='GBK')
            #             except UnicodeDecodeError:
            #                 return '编码错误，请先确定网页编码！现在支持UTF-8，GBK,GB2312，GB18030,'
            # #         except FragmentNotFound, e:
            # #             return e
            # #     except FragmentNotFound, e:
            # #         return e
            # # except FragmentNotFound, e:
            # #     return e
            # return 666
        else:
            url = x['url']
            return 'http://zrb.gotohard.cn/train/?url='+url
class fuzhi:
    def GET(self):
        web.header("Content-Type", "text/html; charset=utf-8")
        x = web.input()
        url = x['url']
        origin_url = x['origin_url']
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            'Referer':origin_url
        }
        req = urllib2.Request(url=url,headers=headers)
        reponse = urllib2.urlopen(req)
        return reponse.read()
class totrain:
    def GET(self):
        # web.header("Content-Type", "text/html; charset=utf-8")
        # x = web.input()
        # url = x['url']
        # renderurl = 'http://zrb.gotohard.cn:8050/render.html?url=' + url
        # reponse = urllib2.urlopen(renderurl)
        # htmlstr = reponse.read()
        # soup = BeautifulSoup(htmlstr, 'html.parser')
        # aaa = []
        # fuzhi_url = 'http://zrb.gotohard.cn/train/fuzhi?url='
        # for i in soup.find_all('link'):
        #     orgin_url = i['href']
        #     if orgin_url
        #     aaa.append(type(orgin_url))
        #     # i['href'] = fuzhi_url+orgin_url

        # return soup.prettify()
        return  6666
        # f = open('/var/www/zrbspider/test/html.html','wb')
        # f.write(htmlstr)
        # a = htmlstr.decode('GB18030').encode('utf-8')
        # href = []
        # for h in a:
        #     return type(h)
    def POST(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header("Content-Type", "Application/json; charset=utf-8")
        data = web.data()
        # f = open('/var/www/zrbspider/test/data2.txt','wb')
        # f.write(data)
        traindata = json.loads(data)
        url = traindata['url']
        tplname = traindata['name'].encode('utf-8')
        inputname = traindata['inputName'].encode('utf-8')
        keys_value = traindata['data']
        annotationItemData = {}
        xpathItemlist = {}
        for i in keys_value:
            if i['signs'] ==1:
                annotationItemData[i['xkey'].encode('utf-8')] = i['xvalue'].encode('utf-8')
            xpathItemlist[i['xkey'].encode('utf-8')] = i['xpath'].encode('utf-8')
        renderurl = 'http://zrb.gotohard.cn:8050/render.html?url=' + url
        filename = time.time()
        filepath = '/var/www/zrbspider/zrbspider/jiegouhua/trainhtml/'+str(int(filename))+'.html'
        tplpath = '/var/www/zrbspider/zrbspider/jiegouhua/tpl/'
        with open('/var/www/zrbspider/zrbspider/jiegouhua/traidata.txt', 'w') as f:
            f.write(str(annotationItemData)+str(xpathItemlist))
        r = urllib2.urlopen(renderurl)
        with open(filepath, 'wb') as f:
            f.write(r.read())

            try:
                res = train(htmlFilePath=filepath, annotationItemData=annotationItemData, tplSaveDir=tplpath,
                            tplSavename=tplname, encoding='utf-8', xpathItemList=xpathItemlist, mode="both")
            except UnicodeDecodeError:
                try:
                    res = train(htmlFilePath=filepath, annotationItemData=annotationItemData, tplSaveDir=tplpath,
                                tplSavename=tplname, encoding='gb2312', xpathItemList=xpathItemlist, mode="both")
                except UnicodeDecodeError:
                    try:
                        res = train(htmlFilePath=filepath, annotationItemData=annotationItemData, tplSaveDir=tplpath,
                                    tplSavename=tplname, encoding='gb18030', xpathItemList=xpathItemlist, mode="both")
                    except UnicodeDecodeError:
                        try:
                            res = train(htmlFilePath=filepath, annotationItemData=annotationItemData,
                                        tplSaveDir=tplpath, tplSavename=tplname, encoding='GBK',
                                        xpathItemList=xpathItemlist, mode="both")
                        except UnicodeDecodeError:
                            return '编码错误，请先确定网页编码！现在支持UTF-8，GBK,GB2312，GB18030,'

        if res['state']=="success":
            r = redis.Redis(localhosturl, port=6379, db=0, password=redis_passwd)
            tpl = {}
            tpl['name'] = tplname
            tpl['inputName'] = inputname
            tpl['tplpath'] = res['tplpath']
            r.lpush('tpl',json.dumps(tpl))
            return json.dumps(res)
        elif res['state']=="error":
            return json.dumps(res)
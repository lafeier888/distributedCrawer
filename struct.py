# -*- coding:utf-8 -*-
import web
import json
import re
from lafeier.AutoStruct import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
urls = (
    "/struct", "struct",
  "/structdata", "structdata"
)
struct_app = web.application(urls, globals())
class struct:
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
    # def POST(self):
    #     web.header('Access-Control-Allow-Origin', '*')
    #     web.header("Content-Type", "Application/json; charset=utf-8")
    #     reload(sys)
    #     sys.setdefaultencoding('utf-8')
    #     # web.header("Content-Type", "text/html; charset=utf-8")
    #     x = web.input(myfile={})
    #     d = web.input()
    #     # j=web.data()
    #     # da=json.loads(d)
    #     filedir = '/var/www/zrbspider/zrbspider/jiegouhua/htmlzip/'  # change this to the directory you want to store the file in.
    #     # return filedir
    #     if 'myfile' in x:  # to check if the file-object is created
    #         filepath = x['myfile'].filename.replace('\\', '/')  # replaces the windows-style slashes with linux ones.
    #         filename = filepath.split('/')[-1]  # splits the and chooses the last part (the filename with extension)
    #         filename = filename.decode('utf-8')
    #         zippath = filedir+filename.encode('utf-8')
    #         # return filepath, filename, chardet.detect(filepath),filepath.decode('utf-8'),chardet.detect(filename),filename.decode('utf-8')
    #         # return zippath
    #         fout = open(zippath, 'wb')  # creates the file where the uploaded file should be stored
    #         fout.write(x['myfile'].file.read())  # writes the uploaded file to the newly created file.
    #         fout.close()  # closes the file, upload complete.
    #         # return "filename: %s\n " % (x['myfile'].filename)
    #         tplname=x['select']
    #         rtplname = tplname.split('.')
    #         zip_un_html = filename.split('.')
    #
    #         # return filename,filename.encode('utf-8'),'aaa'
    #         # return zip_un_html,type(zip_un_html)
    #         savePath = filedir + zip_un_html[0]
    #         savePath = savePath.encode('utf-8')
    #         tplpath='/var/www/zrbspider/zrbspider/jiegouhua/tpl/'+tplname
    #         dictor = {}
    #         num = []
    #         alldata = []
    #         # return zippath.decode('utf-8'), savePath.decode('utf-8'), tplpath.decode('utf-8'), rtplname[0],
    #         try:
    #             alldata = []
    #             alldata = structure(zipFileName=zippath, savePath=savePath, tpl=tplpath,
    #                              tplname=rtplname[0], encoding='utf-8')
    #             num.append(1)
    #             dictor['data1']=alldata
    #         except (UnicodeDecodeError, UnicodeEncodeError):
    #             try:
    #                 alldata = []
    #                 alldata = structure(zipFileName=zippath, savePath=savePath, tpl=tplpath,
    #                                  tplname=rtplname[0], encoding='GB18030')
    #                 num.append(2)
    #                 dictor['data2'] = alldata
    #
    #             except (UnicodeDecodeError, UnicodeEncodeError):
    #                 try:
    #                     alldata = []
    #                     alldata = structure(zipFileName=zippath, savePath=savePath, tpl=tplpath,
    #                                      tplname=rtplname[0], encoding='GB2312')
    #                     num.append(3)
    #                     dictor['data3'] = alldata
    #                 except (UnicodeDecodeError, UnicodeEncodeError):
    #                     alldata = []
    #                     alldata = structure(zipFileName=zippath, savePath=savePath, tpl=tplpath,
    #                                      tplname=rtplname[0], encoding='GBK')
    #                     num.append(4)
    #                     dictor['data4'] = alldata
    #         dirnum = lookThrough(savePath)
    #         dictor['dirnum'] = dirnum
    #         return 666
    #     else:
    #         return 111



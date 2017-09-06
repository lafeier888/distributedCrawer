#encoding=utf-8
# from lafeier import AISpider
from lafeier.AISpider import *
import os.path
from lafeier.template import AnnotationError
from lafeier.template import FragmentNotFound
from lafeier.template import FragmentAlreadyAnnotated
import re
import json
import lafeier.htmlpage
from lxml import etree
from lafeier import Scraper
from HTMLParser import HTMLParser

def getTplSavePath(htmlFilePath=None,tplSaveDir=None,tplSavename=None):
    # 选择模板保存目录
    if not tplSaveDir:
        Savedir = os.path.abspath(defaultTplSaveDir)
    else:
        Savedir = os.path.abspath(tplSaveDir)
    # 选择模板保存的文件名
    if not tplSavename:
        # 带后缀文件名
        filename = os.path.basename(htmlFilePath)
        # 不带后缀文件名
        filename = os.path.splitext(filename)[0]
        filename += ".tpl"
    else:
        filename = tplSavename
    # 拼接保存路径
    tplSavepath = Savedir + os.sep + filename
    return tplSavepath


# ###########################配置项目#############################################3
# 默认编码
defaultEncoding="utf-8"
#默认训练模板保存位置
defaultTplSaveDir="./tpl/"
annotationErrFields=list()

##########################训练（生成模板）相关代码###################################
# 注解训练
def trainByAnnotation(htmlFilePath=None,annotationItemData=None,tplSaveDir=None,tplSavename=None,encoding=None):

    # 判断必须参数是否提供
    if not htmlFilePath:
        return  {
            'state':"error",
            'code':'102',
            'msg':'html文件不存在！'
        }
    if  annotationItemData is None:
        return  {
            'state':"error",
            'code':'101',
            'msg':"训练的字段没有提供！"
        }
    if len(annotationItemData)<=0:
        return {
            'state': "error",
            'code': '110',
            'msg': "不能训练空数据！"
        }
    # 构造模板文件保存路径
    tplSavepath = getTplSavePath(htmlFilePath=htmlFilePath,tplSaveDir=tplSaveDir,tplSavename=tplSavename)
    if not tplSavepath:
       return {
            'state': "error",
            'code': '103',
            'msg': '模板文件保存路径不正确！'
        }
    # 编码
    if not encoding:
        encoding=defaultEncoding
    # 模板生成成功返回模板位置

    try:
        # 所有字段训练成功
        if AISpider.trainFromLocalFiles(os.path.abspath(htmlFilePath),annotationItemData,tplSavepath,encoding):
            return tplSavepath
    except FragmentNotFound,e:
        # 部分或者字段训练失败
        # 失败的字段名
        errFieldName = re.search(r'\'(.*?)\' using', e.message, re.M | re.I).group(1)#训练失败的字段名字
        # 从训练字段列表移除失败的字段

        errFieldName = errFieldName.decode("string_escape")#防止中文，fuck

        try:
            del annotationItemData[errFieldName]
        except:
            return {
                'state': "error",
                'code': '114',
                'msg': '字段名中文问题！'
            }
        # 保存错误的字段名到列表
        annotationErrFields.append(errFieldName)
        # 如果有训练错误的字段，重新训练
        return trainByAnnotation(htmlFilePath=htmlFilePath, annotationItemData=annotationItemData, tplSaveDir=tplSaveDir, tplSavename=tplSavename,
                          encoding=encoding)
    except FragmentAlreadyAnnotated:
        # 同一字段多次训练错误
        return  {
            'state': "error",
            'code': '104',
            'msg': '同一字段多次训练错误！'
        }
# print trainByAnnotation(htmlFilePath="../test.html",annotationItemData={"name":"fry Potter","title":"i am fitle"},encoding="gb2312")

# 把xpath存到模板
def appendXpathToTpl(tplSavePath=None,xpathItemList=None):
    if not tplSavePath:
        return {
            'state':'error',
            'code':'101',
            'msg':'模板文件不存在!'
        }
    if not xpathItemList:
        return {
            'state': 'error',
            'code': '105',
            'msg': 'xpath没提供!'
        }
    # 打开模板文件
    try:
        file = open(os.path.abspath(tplSavePath),'r')
        data = json.load(file)
        file.close()
    except:
        # 模板文件打开失败(不存在)，创建模板文件
        # 说明注解训练失败了，全部字段采用xpath
        # 创建模板保存位置
        if tplSavePath or tplSavePath != "":
            saveDir = os.path.dirname(tplSavePath)
            # 创建模板保存目录
            if not os.path.exists(saveDir):
                os.makedirs(saveDir)
            file = open(os.path.abspath(tplSavePath), 'w')
            file.close()
            data={}
    #加载xpath数据
    data['xpath']={}
    xpathTrainFields=list()
    for(k,v) in xpathItemList.items():
        data['xpath'][k]=v
        xpathTrainFields.append(k)
    data['xpathTrainFields']=xpathTrainFields
    file = open(os.path.abspath(tplSavePath), 'w')
    json.dump(data,file)
    file.close()
    return data
# print appendXpathToTpl(tplSavePath='./tpl/test.tpl',xpathItemList={"name":"//book[@category='WEB'][1]/title","title":"//book[@category='WEB'][2]/title"})

# 集成注解和xpath
def train(htmlFilePath=None,annotationItemData=None,tplSaveDir=None,tplSavename=None,encoding=None,xpathItemList=None,mode="both"):
    # 如果提供了annotation字段
    if  annotationItemData:
        # 注解训练
        res=trainByAnnotation(htmlFilePath=htmlFilePath,annotationItemData=annotationItemData,tplSaveDir=tplSaveDir,tplSavename=tplSavename,encoding=encoding)
        # 注解训练报错，返回错误信息
        if type(res) is  dict  and res['state']=='error' and  res['code']!='110':
            return res
        # 注解训练没有报错
        else:
            # 判断有没有训练失败的字段，有的话吧失败字段用xpath在怼一次,没有直接返回
            xpathItem={}#一个纯净的字典，存放需要用xpath训练的字段
            if  len(annotationErrFields)>0:
                # 有的话就用xpath
                if not xpathItemList:
                    return {
                        'state':'error',
                        'code':'106',
                        'msg':'有字段训练失败，但是并没有提供xpath数据'
                    }
                for key in annotationErrFields:
                    try:
                        xpathItem[key] = xpathItemList[key]
                    except:
                        return {
                            'state': 'error',
                            'code': '113',
                            'msg': '注解训练错误的字段xpath没有提供'
                        }
                #如果注解全部训练失败没有返回模板路径

                if type(res) is  dict:
                    res = getTplSavePath(htmlFilePath=htmlFilePath, tplSaveDir=tplSaveDir, tplSavename=tplSavename)
                appendXpathToTpl(tplSavePath=res,xpathItemList=xpathItem)
                dataFile = open(res,'r')
                data = json.load(dataFile )
                dataFile.close()
                data['mode']=mode
                dataFile=open(res,'w')
                json.dump(data,dataFile)
                dataFile.close()
                return {
                    'state':'success',
                    'tplpath':res#训练成功
                 }
            else:
                return {
                    'state':'success',
                    'tplpath':res#训练成功(全部为注解)
                 }
    elif xpathItemList:
        tplpath = getTplSavePath(htmlFilePath=htmlFilePath,tplSaveDir=tplSaveDir,tplSavename=tplSavename)
        appendXpathToTpl(tplSavePath=tplpath, xpathItemList=xpathItemList)
        dataFile = open(tplpath, 'r')
        data = json.load(dataFile)
        dataFile.close()
        data['mode'] = mode
        dataFile = open(tplpath, 'w')
        json.dump(data, dataFile)
        dataFile.close()
        return {
                    'state':'success',
                    'tplpath':tplpath#训练成功
                 }
    else:
        return {
            'state':'error',
            'code':'107',
            'msg':'注解或者xpath你丫的总的选一种吧？'
        }
# print train(htmlFilePath='../17107.tpl',tplSavename='17107.tpl',annotationItemData={"name":"fry Potter","title":"i am title"},xpathItemList={"name":"//div/a[2]","title":"//book[@category='WEB'][2]/title"})

##############################结构化相关代码##############################

# 注解提取
def annotationStruct(htmlFilePath=None,tplFilePath=None,encoding="gb18030"):
    # 打开模板文件并加载数据
    try:
        tplFileObj = open(os.path.abspath(tplFilePath))
    except IOError:
        return {
            "state":'error',
            'code':'101',
            'msg':'模板文件不存在！'
        }
    try:
        data = json.load(tplFileObj)
        tplFileObj.close()
    except:
        return {
            "state":'error',
            'code':'108',
            'msg':'模板解析失败！！'
        }

    # 加载annotation数据
    try:
        templates = [lafeier.htmlpage.HtmlPage(**x) for x in data['annotation']['templates']]
    except:
        # "state":'error',
        # 'code':'109',
        # 'msg':'注解模板数据不存在！'
        return {

        }
    # 创建scrapely实例
    s = Scraper(templates=templates)
    # 创建htmlpage对象
    try:
        htmlFileObj=  open(os.path.abspath(htmlFilePath))
    except IOError:
        return {
            "state":'error',
            'code':'102',
            'msg':'html文件不存在！'
        }
    page = lafeier.htmlpage.HtmlPage(body=unicode(htmlFileObj.read().decode(encoding)),encoding=encoding)
    htmlFileObj.close()
    # 结构化提取数据
    annotationResult = s.scrape_page(page)
    # 返回数据
    #没有提取到结果返回空数组
    if annotationResult[0]=={}:
        return {}
    #提取到返回字典数组
    res = {}
    for (k,v) in annotationResult[0].items():
        res[k]=v[0]
    return res
# print annotationStruct(htmlFilePath="../17107.html",tplFilePath="./tpl/17107.tpl")

# xpath提取
def xpathStruct(htmlFilePath=None,tplFilePath=None,encoding="utf-8"):
    try:
        tplFileObj = open(os.path.abspath(tplFilePath))
    except IOError:
        return {
            "state":'error',
            'code':'101',
            'msg':'模板文件不存在！'
        }
    # 打开模板并加载数据
    try:
        data = json.load(tplFileObj)
    except Exception,e:
        return {
            "state":'error',
            'code':'108',
            'msg':'模板解析失败！'
        }
    # 加载xpath数据
    try:
        xpathList = data['xpath']
    except Exception,e:
        return {
            "state": 'error',
            'code': '111',
            'msg': 'xpath模板数据不存在！'
        }
    # 解析html文件
    try:
        htmlFileObj = open(os.path.abspath(htmlFilePath))
    except IOError:
        return {
            "state": 'error',
            'code': '102',
            'msg': 'html文件不存在！'
        }
    # try:
        # html = etree.parse(htmlFileObj)
    htmlparse = etree.HTML(htmlFileObj.read().lower().decode(encoding))
    htmlFileObj .close()
    # except Exception,e:
    #     return {
    #         "state": 'error',
    #         'code': '112',
    #         'msg': 'html解析失败！'+e.message
    #     }

    # 结构化提取数据
    xpathResult = {}
    # htmlparse = HTMLParser()
    for (k,v) in xpathList.items():
        value = ""
        for v in htmlparse.xpath(v):
            value += v.xpath('string(.)')
        if value!="":
            xpathResult[k] = value
    return xpathResult
# print xpathStruct(htmlFilePath="../17107.html",tplFilePath="./tpl/17107.tpl")

# 结构化集成
def struct(htmlFilePath=None,tplFilePath=None,encoding="utf-8"):
    annotationResult = annotationStruct(htmlFilePath=htmlFilePath, tplFilePath=tplFilePath,encoding=encoding)

    # 有错误信息就返回
    try:
        if type(annotationResult) is  dict and annotationResult['state']=="error"  :

            return annotationResult
    except:
        pass

    xpathResult = xpathStruct(htmlFilePath=htmlFilePath, tplFilePath=tplFilePath,encoding=encoding)
    # 有错误信息返回
    try:
        if type(xpathResult) is  dict and xpathResult['state']=='error'  :
            if xpathResult['code']=="111":
                #全部为直接训练的话不用返回xpath数据
                xpathResult={}
            else:
                return xpathResult
    except:
        pass

    #annotation和xpath都没有报错
    return {
        "state":"success",
        "data":dict(xpathResult.items() + annotationResult.items())
    }
# print struct(htmlFilePath="../17107.html",tplFilePath="./tpl/17107.tpl",encoding='gb18030')

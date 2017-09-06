#-*-coding:UTF-8-*-
import json

from w3lib.util import str_to_unicode

from lafeier.htmlpage import HtmlPage, page_to_dict, url_to_page
from lafeier.template import TemplateMaker, best_match
from lafeier.extraction import InstanceBasedLearningExtractor
from lafeier.version import __version__
import os

class Scraper(object):

    def __init__(self, templates=None):
        """Initialize an empty scraper."""
        self._templates = templates or []
        self._ex = None

    @classmethod
    def fromfile(cls, file):
        """Initialize a scraper from a file previously stored by tofile()
        method.
        """
        templates = [HtmlPage(**x) for x in json.load(file)['templates']]
        return cls(templates)

    def tofile(self, file):
        """Store the scraper into the given file-like object"""
        tpls = [page_to_dict(x) for x in self._templates]
        json.dump({'templates': tpls}, file)

    def add_template(self, template):
        self._templates.append(template)
        self._ex = None

    def train_from_htmlpage(self, htmlpage, data):
        assert data, "Cannot train with empty data"
        tm = TemplateMaker(htmlpage)
        for field, values in data.items():
            if (isinstance(values, (bytes, str)) or
                    not hasattr(values, '__iter__')):
                values = [values]
            for value in values:
                value = str_to_unicode(value, htmlpage.encoding)
                tm.annotate(field, best_match(value))
        self.add_template(tm.get_template())

    def train(self, url, data, encoding=None):
        page = url_to_page(url, encoding)
        self.train_from_htmlpage(page, data)

    def scrape(self, url, encoding=None):
        page = url_to_page(url, encoding)
        return self.scrape_page(page)

    def scrape_page(self, page):
        if self._ex is None:
            self._ex = InstanceBasedLearningExtractor((t, None) for t in
                    self._templates)
        return self._ex.extract(page)[0]

# AISpider
# Author:lafeier
# class AISpider:
#     @classmethod
#     # 从本地文件训练
#     def trainFromLocalFiles(cls, htmlFilepath="", annotationItemData="", saveFilename="", encoding='utf-8'):
#         s = Scraper()
#         file = open(htmlFilepath)
#         content = file.read()
#         page = HtmlPage(body=unicode(content.decode(encoding)), encoding=encoding)
#         s.train_from_htmlpage(page, annotationItemData)
#
#         if (saveFilename != ""):
#             saveDir = os.path.dirname(saveFilename)
#             # 创建模板保存目录
#             if not os.path.exists(saveDir):
#                 os.makedirs(saveDir)
#             # 判断是否模板已存在
#             try:
#                 file = open(saveFilename, "r")
#                 data = json.load(file)  # 存在就直接读
#                 data['annotation'] = {}
#                 # 关闭文件
#                 file.close()
#             except IOError:  # 不存在创建
#                 data = {}
#                 data['annotation'] = {}
#
#             tpls = [page_to_dict(x) for x in s._templates]
#
#             data['annotation']['templates'] = tpls
#             #在模板中标出那些字段是annotation方式的
#             annotationTrainFields=list()
#             for(k,v) in annotationItemData.items():
#                 annotationTrainFields.append(k)
#             data['annotationTrainFields']=annotationTrainFields
#             # 输出模板信息
#             file = open(saveFilename, "w")
#             json.dump(data, file)
#             # 关闭文件
#             file.close()
#         return s
#
#     @classmethod
#     def trainFromUrls(cls, items, saveFilename="", encoding='utf-8'):
#         s = Scraper()
#         for item in items:
#             s.train(item["url"], item["data"], encoding=encoding)
#         if (saveFilename != ""):
#             file = open(saveFilename, "wb")
#             print file
#         # s.tofile(file)
#         return s
#
#     # 从以存在的模板获取一个Scrapely实例
#     @classmethod
#     def getScrapelyFromTpl(cls, filename):
#         file = open(filename, "rb")
#         return Scraper.fromfile(file)
#
#     # 将本地网页转成Scrapely需要的Page对象
#     @classmethod
#     def fileToPage(csl, filename, encoding='utf-8'):
#         file = open(filename)
#         content = file.read()
#         return HtmlPage(body=unicode(content.decode(encoding)), encoding=encoding)

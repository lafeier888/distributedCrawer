import requests
import os
import time

filedir = os.path.dirname(__file__)
url = 'https://item.taobao.com/item.htm?spm=a310p.7395725.1998460392.1.ffca6c0RPkCO6&id=549869514793'
# renderurl = 'http://zrb.gotohard.cn:8050/render.html?url='+url
# return renderurl
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
r = requests.get(url, headers=headers)
print r.status_code, 7855666
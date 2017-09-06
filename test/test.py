
#coding:utf-8
import zipfile
def extract(zipFileName,savePath):
	z =  zipfile.ZipFile(zipFileName)
	for p in z.namelist():
		print p
		z.extract(p, savePath)
	z.close()
extract("拉斐尔.zip","/var/www/zrbspider/")

# coding=utf-8
import urllib2
import urllib
#import requests
import tornado.httpclient as hc
import re
from lxml import html
import csv
import sys
import requests
from src.analyze.datafetch import *
from src.util.csvwriter import *
reload(sys)
sys.setdefaultencoding('utf8')
from lxml.html.clean import Cleaner

class lianjiaspider():
    def readcookies(self,filename):
        cookies={}
        with open(filename) as f:
            for line in f.readlines():
                key, value = line.strip().split('=', 1)
                cookies[key] = value
            #print cookies
        f.close()
        return cookies
    def getHtmlbyreq(self,url,cookies=None,data=None):
        if data!=None and isinstance(data,dict):
            r = requests.get(url,data)
        if cookies!=None and isinstance(cookies,dict):
            r = requests.get(url,cookies=cookies)
        if r.status_code==200:
            return r.content
        else:
            return None
    def getHtml(self,url):
        page = urllib2.urlopen(url)
        mypage = page.read()
        mypage=unicode(mypage, "utf-8")
        cleaner = Cleaner(style=True, scripts=True, page_structure=False, safe_attrs_only=False)  # 清除掉CSS等
        return cleaner.clean_html(mypage)
    def datafinder(self,mypage,model=None):
        tree=html.fromstring(mypage)
        if model!=None:
            return tree.xpath(model)
    def savetofile(self,mypage,file):
        with open(file,'w+') as f:
            f.write(mypage)

def catchlianjiadata():
    baseurl='http://sh.lianjia.com/ershoufang/'
    s=lianjiaspider()
    content=s.getHtml(baseurl)
    tree = html.fromstring(content)
    districtname=tree.xpath(u"//div[@class='option-list gio_district']/a/@gahref")[1:-1]
    for district in districtname:
        print district
        basedisurl=baseurl+district
        districtcontent=s.getHtml(basedisurl)
        tree = html.fromstring(districtcontent)
        areaname=tree.xpath(u"//div[@class='option-list sub-option-list gio_plate']/a/@gahref")[1:]
        for area in areaname:
            print area
            csvfile,writer=csvwriter('e:\lianjia\lianjia'+district+'_'+area+'.csv')
            baseareaurl=baseurl+area
            areacontent=s.getHtml(baseareaurl)
            tree = html.fromstring(areacontent)
            tree.text_content()
            itemnums=tree.xpath(u"//div[@class='secondcon fl']/ul/li[3]/span[2]/strong/text()")
            if itemnums!=0:
                pagenum=(int(itemnums[0])/20)+1
            else:
                pagenum=0
            print baseareaurl
            if pagenum==None:
                pagenum=0
            for j in range(0,pagenum):
                if j+1>1:
                    baseareaurlwithpage=baseareaurl+'/d'+str(j+1)
                    areacontentwithpage=s.getHtml(baseareaurlwithpage)
                    tree = html.fromstring(areacontentwithpage)
                rowdata=analyzelianjiasecondhand(tree)
                writer.writerows(rowdata)
            csvfile.close()


if __name__=='__main__':
    baseurl = 'http://sh.lianjia.com/ershoufang/gumei/d45'
    # headers = {'content-type': 'application/json'}
    s = lianjiaspider()
    content = s.getHtml(baseurl)
    csvfile = file('e:\lianjia\lianjiatest.csv', 'wb')
    writer = csv.writer(csvfile)
    tree = html.fromstring(content)
    writer.writerows(rowlst)
        #print str(e.xpath(u"//div[@class='where']/span[2]/text()")).encode('utf8').strip()
    csvfile.close()

# coding=utf-8
import urllib
import urllib2
#import requests
import tornado.httpclient as hc
import re
from lxml import html
import csv
import sys
import requests

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
            print 200
        return r.content

    def getHtml(self,url):
        #proxy = 'http://%s:%s@%s' % ('jiangxiaowei-006','#EDC7ujm','10.228.46.21:8002')
        #opener = urllib2.build_opener(urllib2.ProxyHandler({'http':'http://jiangxiaowei-006:#EDC7ujm@10.228.46.21:8002'}))
        #urllib2.install_opener(opener)
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
    #headers = {'content-type': 'application/json'}
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
            csvfile = file('e:\lianjia\lianjia'+district+'_'+area+'.csv', 'wb')
            writer = csv.writer(csvfile)
            baseareaurl=baseurl+area
            areacontent=s.getHtml(baseareaurl)
            tree = html.fromstring(areacontent)
            tree.text_content()
            itemnums=tree.xpath(u"//div[@class='secondcon fl']/ul/li[3]/span[2]/strong/text()")
            #pagenum=s.page_counter(areacontent)
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
                xiaoquname=tree.xpath(u"//div[@class='where']/a/span/text()")
                fangxing=tree.xpath(u"//div[@class='where']/span[1]/text()")
                mianji=tree.xpath(u"//div[@class='where']/span[2]/text()")
                lclst=[]
                louceng = tree.xpath(u"//div[@class='con']/span[1]")
                for lc in louceng:
                    lclst.append(lc.tail.encode('utf8').strip())
                cxlst=[]
                chaoxiang=tree.xpath(u"//div[@class='con']/span[2]")
                for cx in chaoxiang:
                    cxlst.append(cx.tail.encode('utf8').strip())
                    #fangsubway=tree.xpath(u"//span[@class='fang-subway-ex']/span/text()")
                    #taxfreeex=tree.xpath(u"//span[@class='taxfree-ex']/span/text()")
                print len(cxlst)
                print '----------------'
                print len(lclst)
                prices=tree.xpath(u"//div[@class='price']/span/text()")
                perprice=tree.xpath(u"//div[@class='price-pre']/text()")
                    #print type(perprice)
                    #seennum=tree.xpath(u"//div[@class='square]/div/span/text()")
                retlst=[]
                if j+1!=pagenum:
                    for i in range(20):
                        rowdata=(xiaoquname[i].encode('utf-8'),fangxing[i].encode('utf-8'),mianji[i].encode('utf-8'),lclst[i],cxlst[i],prices[i].encode('utf-8'),perprice[i].encode('utf-8'))
                        retlst.append(rowdata)
                else:
                    for i in range(len(xiaoquname)):
                        rowdata=(xiaoquname[i].encode('utf-8'),fangxing[i].encode('utf-8'),mianji[i].encode('utf-8'),lclst[i],cxlst[i],prices[i].encode('utf-8'),perprice[i].encode('utf-8'))
                        retlst.append(rowdata)
                writer.writerows(retlst)
            csvfile.close()


if __name__=='__main__':
    baseurl = 'http://sh.lianjia.com/ershoufang/gumei/d45'
    # headers = {'content-type': 'application/json'}
    s = lianjiaspider()
    content = s.getHtml(baseurl)
    tree = html.fromstring(content)
    elemenlst=tree.find_class('info-panel')
    print elemenlst
    csvfile = file('e:\lianjia\lianjiatest.csv', 'wb')
    writer = csv.writer(csvfile)
    rowlst=[]
    for e in elemenlst:
        #dataarr=e.text_content()
        lst=[]
        lst.append(e.find_class('nameEllipsis')[0].text_content())
        #print e.xpath(u"//div/div/span[2]")
        lst.append(''.join(e.find_class('con')[0].text_content().strip().split()))

        subway= e.find_class('fang-subway-ex')
        if len(subway)==0:
            lst.append('')
        else:
            lst.append(subway[0].text_content())

        taxfree=e.find_class('taxfree-ex')
        if len(taxfree)==0:
            lst.append('')
        else:
            lst.append(taxfree[0].text_content())

        haskey=e.find_class('haskey-ex')
        if len(haskey)==0:
            lst.append('')
        else:
            lst.append(haskey[0].text_content())
        print lst
        rowlst.append(lst)
        print '#######################'
        #print dataarr
    writer.writerows(rowlst)
        #print str(e.xpath(u"//div[@class='where']/span[2]/text()")).encode('utf8').strip()
    csvfile.close()


import requests
class spiders():
    def readcookies(self,filename):
        cookies={}
        with open(filename) as f:
            for line in f.readlines():
                key, value = line.strip().split('=', 1)
                cookies[key] = value
            #print cookies
        f.close()
        return cookies
    def getHtml(self,url,cookies=None,data=None):
        if data!=None and isinstance(data,dict):
            r = requests.get(url,data)
        if cookies!=None and isinstance(cookies,dict):
            r = requests.get(url,cookies=cookies)
        else:
            print 'cookies must be dict type'
        if r.status_code==200:
            print 200
        return r.content


if __name__=="__main__":
    url='http://sh.lianjia.com/chengjiao/'
    s=spiders()
    cok=s.readcookies("E:\lianjia\lianjiacookies.txt")
    page=s.getHtml(url,cookies=cok)
    print page
    with open("E:\lianjia\lianjiatestuser.html", 'wb') as f:
        f.write(page)
    f.close()
#/usr/bin/python
#coding=utf-8

import urllib2
import urllib
import re
from sets import Set
import json
from productInfo import ProductInfo
from nikeHtmlParser import NikeHTMLParser

top_url = 'http://store.nike.com/cn/zh_cn/'
second_url = 'http://store.nike.com/html-services/gridwallData?country=CN&lang_locale=zh_CN&gridwallPath=n/1j5&pn='
all_products_url = set()
patten = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", re.IGNORECASE)
keyword = 'http://store.nike.com/cn/zh_cn/pd'

def fetch_all_procduct_url(all_products_url):
    fetch_mainpage(all_products_url)
    count = 1
    while 1:
        if fetch_nextpage(all_products_url,count):
            count = count + 1
            continue
        else:
            break

 #   print_all_urls(all_products_url)

def fetch_mainpage(all_products_url):
    try:
        request = urllib2.urlopen(top_url)
    except HTTPError, e:
        print "Http Error code" ,e.code
    except URLError, e:
        print "Reason Error code" ,e.code
    else:
        html_string = request.read()
        all_urls = patten.findall(html_string)
        for url in all_urls:
            if keyword in url:
                all_products_url.add(url)
    return;

def fetch_nextpage(all_products_url,count):
    new_fetch_url = second_url + str(count)
    request = urllib2.urlopen(new_fetch_url)
    result = request.read()
    products_url = patten.findall(result)
    for url in products_url:
        if keyword in url:
            all_products_url.add(url)

    if 'nextPageDataService' not in result:
        return False
    else:
        return True


def print_all_urls(all_products_url):
    for url in all_products_url:
        print url
    pass

def fetchDataByPatten(patten, input_data):
    m = re.search(patten, input_data)
    if m:
       return m.group(0)
    else:
        pass

def fetch_product_info(url):
    p = ProductInfo('')
    m = fetchDataByPatten("pid-\w+",url)
    if m :
        p.pid = m[4:]
    else:
        print "Error: can't get Pid"

    m = fetchDataByPatten("pgid-\w+",url)
    if m:
        p.pgid = m[5:]
    else:
        print "Error: can't get Pgid"

    try:
        request = urllib2.urlopen(url)
        result = request.read()
    except urllib2.URLError, e:
        print "Reason Error code" ,e.reason
        print "Error: Url", url
    else:
        nikeParser = NikeHTMLParser()
        bodyPart = result[result.index("<body"):result.index("</body>")]
        nikeParser.feed(bodyPart)

        for size in nikeParser.sizeList:
            p.addStockList(size)

        p.price = nikeParser.price + ',' + nikeParser.originPrice
        p.desc = nikeParser.desc
        p.style = nikeParser.style
        p.titleDesc = nikeParser.titleDesc
        p.url = url
        jsonProduct = p.toJson()
        fo = open("data.txt", 'a')
        fo.write(jsonProduct)
        fo.write('\n')
        fo.close()
        print jsonProduct

if __name__=="__main__":
    print 'enter main function'
    fetch_all_procduct_url(all_products_url)
    print "Total products number", len(all_products_url)
    loop = 0
    for url in all_products_url:
        loop = loop + 1
        print "Num of", loop
        fetch_product_info(url)

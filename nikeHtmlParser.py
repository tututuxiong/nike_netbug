#/usr/bin/python
#coding=utf-8

from HTMLParser import HTMLParser
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

price_patten_rule = "\d+"
style_patten_rule = ":.*"

class NikeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.priceFlag= False
        self.originPriceFlag= False
        self.styleFlag = False
        self.style = ''
        self.descFlag = False
        self.titleDescFlag = False
        self.titleDesc = ''
        self.sizeFlag= False
        self.price = ''
        self.originPrice = ''
        self.desc = ''
        self.sizeList= []

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            for attr in attrs:
                if "exp-pdp-local-price js-pdpLocalPrice" in attr[1]:
                    self.priceFlag = True

                if "exp-style-color" in attr[1]:
                    self.styleFlag = True

                if "exp-pdp-overridden-local-price" in attr[1]:
                    self.originPriceFlag = True


        if tag == 'option':
            for attr in attrs:
                if attr[0] == "name":
                    self.sizeFlag = True

        if tag == 'h1':
            for attr in attrs:
                if 'exp-product-title' in attr[1]:
                    self.descFlag = True

        if tag == "h2":
            for attr in attrs:
                if 'exp-product-subtitle' in attr[1]:
                    self.titleDescFlag = True


    def handle_data(self, data):
        if self.priceFlag:
            m = re.search(price_patten_rule,data)
            if m:
                self.price = m.group(0)
            self.priceFlag= False

        if self.originPriceFlag:
            m = re.search(price_patten_rule,data)
            if m:
                self.originPrice = m.group(0)
            self.originPriceFlag = False

        if self.sizeFlag:
            self.sizeList.append(data.strip())
            self.sizeFlag = False

        if self.titleDescFlag:
            self.titleDesc = data
            self.titleDescFlag = False

        if self.descFlag:
            self.desc = data
            self.descFlag = False

        if self.styleFlag:
            m = re.search(style_patten_rule,data)
            if m:
                self.style = m.group(0)
            self.styleFlag= False

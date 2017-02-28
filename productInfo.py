#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
import random
import json
class ProductInfo:
    def __init__(self, pid):
        self.pid = pid
        self.pgid = ''
        self.url = ''
        self.style = ''
        self.titleDesc = ''
        self.desc = ''
        self.price = ''
        self.stock= ''
        self.sp = ''
        self.sp_url = ''
        self.sp_url = ''
        self.sp_starttime = ''
        self.sp_endtime = ''
        self.coupon= ''
        self.price = ''
        self.sizeList = []

    def addStockList(self, size, num = '0'):
        if num != '0':
            self.stock = self.stock + size + ':' + num
        else:
            self.stock = self.stock + size + ':' + str(random.randint(1, 10))

        self.stock = self.stock + ', '
        self.sizeList.append(size)

    def toJson(self):
        dict={'url':self.url,'guid':self.style,'title':self.desc,
              'kind':self.titleDesc, 'price':self.price,
              'coupon':self.coupon, 'sp':self.sp,
              'sp_url':self.sp_url, 'sp_starttime':self.sp_starttime,
              'sp_endtime':self.sp_endtime, 'stock':self.stock}
        return json.dumps(dict)

    def getEmptyInfo(self):
        if len(self.sizeList) == 0:
            return ''
        else:
            return "有货"

"""
capture data before some date from certain m_weibo urls
@author: Dannie Lei
@date: 2018/7/20
"""

import requests
import json
from datetime import datetime
from jt.utils.misc import Logger

Log = Logger('WeiboCrawler')

class WeiboCrawler(object):

    def __init__(self, prefix_, end_date_, page_=1):        
        self._prefix = prefix_         
        self._end_date = end_date_     
        self._page = page_
        self.__url = self._prefix.format(page_)

    @property
    def get_url(self):
        return self.__url

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, prefix_):
        self._prefix = prefix_
    
    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, page_):
        self._page = page_
        self.__url = self.prefix.format(page_)

    @property
    def enddate(self):
        return self._end_date

    @enddate.setter
    def enddate(self, end_date_):
        self._end_date = end_date_

    def get_weibo(self):        
        response = requests.get(self.get_url)
        ob_json = json.loads(response.text)
        list_crads0 = ob_json.get('data')
        list_crads = list_crads0.get('cards')
        return list_crads

    def get_products(self):
        list_cards = self.get_weibo()
        end_date = datetime.strptime(self.enddate, "%m-%d")
        for card in list_cards:
            if card.get('card_type') == 9:
                date_str = card.get('mblog').get('created_at')
                if '-' in date_str:
                    # 判断日期
                    current_date = datetime.strptime(date_str, "%m-%d")
                    if current_date < end_date:
                        break
                    Log.info('时间 %s' % date_str)
                else:Log.info('时间 %s' % date_str)
                #获取日期
                text = card.get('mblog').get('text')
                if '【' in text:
                    b_loc = text.index('【')
                    try:
                        e_loc = text.index('】') + 1
                    except ValueError:
                        e_loc = len(text)
                    text=text[b_loc:e_loc]
                Log.info('事件 %s' % text)
                # 获取事件
                url = card.get('scheme')
                Log.info('链接 %s' % url)
                # 获取链接
        return date_str

    def list_contents(self):          
        curdate = self.get_products()
        if '-' in curdate:
            while datetime.strptime(curdate, "%m-%d")  >= datetime.strptime(self.enddate, "%m-%d"):
                self.page =self.page + 1
                curdate = self.get_products()
        else:
            while True:
                self.page = self.page + 1
                curdate = self.get_products()


if __name__ == '__main__':
    weibo = WeiboCrawler(r'https://m.weibo.cn/api/container/getIndex?type=uid&value=3802136340&containerid=1076033802136340&page={}','07-01')
    weibo.list_contents()



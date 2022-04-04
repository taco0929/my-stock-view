from catalog.models import *
from .setting import *
import re
import datetime

DATE_DICTIONARY = {
    'm' : datetime.timedelta(days=30),       # month
    'w' : datetime.timedelta(days=7),       # week
    'd' : datetime.timedelta(days=1),       # day
    'h' : datetime.timedelta(minutes=60),       # hour
}

def parse_time_period(s)-> dict():
    return re.search(r'(?P<d>\d+)(?P<s>\w+)',s).groupdict()

def news_ctrl():
    while News.objects.count() > MAX_NEWS_NUMBER:
        News.objects.last().delete()
    print('Finished maintain db-News')
    return

def hp_ctrl():
    delta = DATE_DICTIONARY[parse_time_period(OLDEST_HIS_PRICE)['s']]*int(parse_time_period(OLDEST_HIS_PRICE)['d'])
    now = datetime.datetime.now()
    for his in HistoryPrice.objects.all().order_by('date_time'):
        if now - his.date_time > delta:
            his.delete()
        else:   
            print('Finished maintain db-HistoryPrice')
            return

def hp_sum_ctrl():
    delta = DATE_DICTIONARY[parse_time_period(OLDEST_HIS_PRICE_SUM)['s']]*int(parse_time_period(OLDEST_HIS_PRICE_SUM)['d'])
    now = datetime.datetime.now()
    for his in HistoryPriceSummary.objects.all().order_by('date'):
        if now - datetime.datetime.combine(his.date,datetime.datetime.min.time()) > delta:
            his.delete()
        else:   
            print('Finished maintain db-HistoryPriceSummary')
            return
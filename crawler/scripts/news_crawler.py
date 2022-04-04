from GoogleNews import GoogleNews
from catalog.models import Stock, News
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.db.models import Q
import time
import re

def get_news(*stock_list,period='1d'):
    if not stock_list:  
        stock_list = Stock.objects.all()
        
    for stock in stock_list:
        
        code = stock
        if type(stock) != Stock:
            stock = Stock.objects.filter(Q(name=stock)|Q(code=stock)).first()
        if not stock:
            # Need to update logging
            print(f'Stock object ({code}) not found! Update DB or check the stock lists/spellings')
            continue
        del code
        
        q = stock.name
        news_list = GoogleNews(lang="zh-TW",period=period,region='TW')
        news_list.search(q)
        
        for news in news_list.results():
            print(news['title'])
            try:
                n = News.objects.get(title=news['title'])
            except ObjectDoesNotExist:
                if re.search(f'{q}',news['title']):
                    n = News(
                        title=news['title'],
                        url=news['link'],
                        content=news['desc'],
                        date_time=news['datetime'] or datetime.datetime.now(),
                    )
                    n.save()
                    n.related_stock.add(stock)
                
                continue
            n.related_stock.add(stock)
        time.sleep(1)
            
            
                
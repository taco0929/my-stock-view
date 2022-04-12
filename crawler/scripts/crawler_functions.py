import requests
import pandas as pd
from catalog.models import HistoryPrice, Stock,Sector, StockInformation, HistoryPriceSummary
from django.core.exceptions import ObjectDoesNotExist
import datetime
import yfinance as yf
import twstock
from django.core.exceptions import ObjectDoesNotExist
import time
from .setting import *
import logging
logger = logging.getLogger('testlogger')

def get_stock_list():
    logger.info('Starting...(get_stock_list)')
    '''
    Build up data-base
    建立資料庫
    '''
    try:
        link = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
        html_doc = requests.get(link).text
        df = pd.read_html(html_doc)[0]
        df[0] = df[0].str.split()
        
        if STOCK_LIST:  
            for i,v in enumerate(STOCK_LIST):
                STOCK_LIST[i] = str(v)
            STOCK_LIST.sort()
            logger.info('STOCK_LIST sorted' )
        else:   logger.info('STOCK_LIST is empty, loading every stock')
        
        for i in range(2,len(df)):
            if STOCK_LIST:
                if STOCK_LIST[0] not in df.iloc[i,0]:
                    continue
                
                logger.info(f'Process: {STOCK_LIST[0]}')
                sector, created = Sector.objects.get_or_create(name=df.iloc[i,4])
                logger.info(f'Loading')
                s,created = Stock.objects.get_or_create(name=df.iloc[i,0][1],code=df.iloc[i,0][0],sector=sector)
                if created: logger.info(f'Process: {STOCK_LIST[0]} created')
                get_stock_information(s)
                STOCK_LIST.pop(0)
            else:
                logger.info(f'Process: {STOCK_LIST[0]}')
                sector, created = Sector.objects.get_or_create(name=df.iloc[i,4])
                logger.info(f'Loading ')
                s,created = Stock.objects.get_or_create(name=df.iloc[i,0][1],code=df.iloc[i,0][0],sector=sector)
                if created: logger.info(f'Process: {STOCK_LIST[0]} created')
                get_stock_information(s)
                
    except Exception as e:
        print(globals())
        print(locals())
        raise e
    
        

def get_stock_information(s:Stock,start='2022-1-1',end=datetime.date.today()):
    '''
    Use yahoo finance api to get and stock information
    使用yahoo finance api獲取股票資訊
    '''
    logger.info(f'Updating info for {s}')
    try: 
        ticker = yf.Ticker(f'{s.code}.TW')
        inf = ticker.info
        his = ticker.history(period='max',start=start,end=end)
        fields = {
            'longBusinessSummary':'',
            'enterpriseValue':'',
            'returnOnEquity':'',
            'returnOnAssets':'',
            'totalRevenue':'',
            'revenueGrowth':'',
            'revenuePerShare':'',
            }
        for field in fields:
            fields[field] = inf[field] if field in inf else None
            
        s_inf, created= StockInformation.objects.get_or_create(stock=s)
        s_inf.business_describ=fields['longBusinessSummary']
        s_inf.market_value=fields['enterpriseValue']
        s_inf.roe=fields['returnOnEquity']
        s_inf.roa=fields['returnOnAssets']
        s_inf.revenue=fields['totalRevenue']
        s_inf.revenue_growth=fields['revenueGrowth']
        s_inf.revenue_per_share=fields['revenuePerShare']
        s_inf.save()
    except Exception as e:
        print(globals())
        print(locals())
        raise e
    logger.info(f'Finished updating info for {s}')
    get_stock_his_price(s,his)

def get_stock_his_price(stock:Stock,df):
    '''
    Pass in pandas.DataFrame (yfinance.Tickers.history()) to save history price summary
    傳入 pandas.DataFrame (yfinance.Tickers.history()) 以取得盤中價格資訊
    '''
    logger.info(f'Start getting his price for {stock}')
    try:
        
        for date in df.index:
            if not HistoryPriceSummary.objects.filter(stock=stock,date=date):
                if type(date) ==pd.Timestamp:
                    date = date.date()
                if type(date) == datetime.date:
                    date = str(date)
                his_p = HistoryPriceSummary(
                    stock=stock,
                    date=datetime.datetime.strptime(date+' +0800', '%Y-%m-%d %z'),
                    open=df.loc[date,'Open'],
                    high=df.loc[date,'High'],
                    low=df.loc[date,'Low'],
                    close=df.loc[date,'Close']
                )
                his_p.save()
        logger.info(f'Finished getting his price for {stock}')
    except Exception as e:
        print(globals())
        print(locals())
        raise e
        

def get_stock_cur_price(*stock_list):
    '''
    Get current price
    獲取現在股價
    '''
    try:
        if not stock_list:   
            stock_list = Stock.objects.all()
        for stock in stock_list:
            try:
                if type(stock) != Stock:
                    stock = Stock.objects.get(code=stock)
            except ObjectDoesNotExist:
                print(f'Stock item ({stock}) does not exist!')
                continue

                
            p = twstock.realtime.get(stock.code)
            if p['realtime']['latest_trade_price'] == '-':
                p['realtime']['latest_trade_price'] = p['realtime']['best_bid_price'][0]
            p['info']['time'] = datetime.datetime.strptime(p['info']['time']+' +0800','%Y-%m-%d %H:%M:%S %z')
            if not HistoryPrice.objects.filter(stock_code=stock,date_time=p['info']['time']):
                h = HistoryPrice(
                    stock_code=stock,
                    date_time=p['info']['time'],
                    price=p['realtime']['latest_trade_price']
                    )
                h.save()
                print(f'{stock}.........Done')
            else:
                continue
    except Exception as e:
        print(globals())
        print(locals())
        raise e 
    
def update_exist_stock_hp_sum(*stock_list):
    
    try:
        if not stock_list:   
            stock_list = Stock.objects.all()
            
        for stock in stock_list:
            try:
                if type(stock) != Stock:
                    stock = Stock.objects.get(code=stock)
            except ObjectDoesNotExist:
                print(f'Stock item ({stock}) does not exist!')
                continue
            d = twstock.realtime.get(stock.code)
            if d['realtime']['latest_trade_price'] == '-':
                d['realtime']['latest_trade_price'] = d['realtime']['best_bid_price'][0]
            his_p = HistoryPriceSummary(
                    stock=stock,
                    date=datetime.datetime.strptime(d['info']['time'].split()[0]+' +0800','%Y-%m-%d %z'),
                    open=float(d['realtime']['open']),
                    high=float(d['realtime']['high']),
                    low=float(d['realtime']['low']),
                    close=float(d['realtime']['latest_trade_price']),
                )
            his_p.save()
            print(f'{stock}.........Done')
            time.sleep(0.5)
    except Exception as e:
        print(globals())
        print(locals())
        raise e 
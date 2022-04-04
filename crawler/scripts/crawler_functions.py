import requests
import pandas as pd
from catalog.models import HistoryPrice, Stock,Sector, StockInformation, HistoryPriceSummary
from django.core.exceptions import ObjectDoesNotExist
import datetime
import yfinance as yf
import twstock
from django.core.exceptions import ObjectDoesNotExist
import time

def get_stock_list():
    '''
    Build up data-base
    建立資料庫
    '''
    link = 'https://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
    html_doc = requests.get(link).text
    df = pd.read_html(html_doc)[0]
    df[0] = df[0].str.split()

    for i in range(2,len(df)):
        try:
            sector = Sector.objects.get(name=df.iloc[i,4])
        except ObjectDoesNotExist:
            sector = Sector(name=df.iloc[i,4])
            sector.save()
        if not Stock.objects.filter(code=df.iloc[i,0][0]):
            s = Stock(name=df.iloc[i,0][1],code=df.iloc[i,0][0],sector=sector)
            print(s.sector)
            print(s)
            s.save()
            get_stock_information(s)
        

def get_stock_information(s:Stock,start='2022-1-1',end=datetime.date.today()):
    '''
    Use yahoo finance api to get and stock information
    使用yahoo finance api獲取股票資訊
    '''
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
    s_inf = StockInformation(
        stock=s,
        business_describ=fields['longBusinessSummary'],
        market_value=fields['enterpriseValue'],
        roe=fields['returnOnEquity'] ,
        roa=fields['returnOnAssets'],
        revenue=fields['totalRevenue'],
        revenue_growth=fields['revenueGrowth'],
        revenue_per_share=fields['revenuePerShare'],
        )

    s_inf.save()
    get_stock_his_price(s,his)

def get_stock_his_price(stock:Stock,df):
    '''
    Pass in pandas.DataFrame (yfinance.Tickers.history()) to save history price summary
    傳入 pandas.DataFrame (yfinance.Tickers.history()) 以取得盤中價格資訊
    '''
    
    for date in df.index:
        his_p = HistoryPriceSummary(
            stock=stock,
            date=date,
            open=df.loc[date,'Open'],
            high=df.loc[date,'High'],
            low=df.loc[date,'Low'],
            close=df.loc[date,'Close']
        )
        his_p.save()
        

def get_stock_cur_price(stock):
    '''
    Get current price
    獲取現在股價
    '''
    p = twstock.realtime.get(stock)
    h = HistoryPrice(stock_code=stock,date_time=p['info']['time'],price=p['realtime']['latest_trade_price'])
    h.save()
    
def update_exist_stock_his_price(*stock_list):
    if not stock_list:   
        stock_list = Stock.objects.all()
        
    for stock in stock_list:
        try:
            if type(stock) != Stock:
                stock = Stock.objects.get(stock)
        except ObjectDoesNotExist:
            print(f'Stock item ({stock}) does not exist!')
            continue
        d = twstock.realtime.get(stock.code)
        his_p = HistoryPrice(
                stock=stock,
                date=d['info']['time'].split()[0],
                open=d['open'],
                high=d['high'],
                low=d['low'],
                close=d['realtime']['latest_trade_price']
            )
        his_p.save()
        time.sleep(0.5)
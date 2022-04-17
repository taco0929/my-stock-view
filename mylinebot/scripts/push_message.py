from .setup import *
import pytz
import datetime
from .get_line_user import getLineUser
from linebot.models import TextSendMessage
import logging
import pytz
from my_stock_view import settings
from catalog.models import UserLineID
logger = logging.getLogger('testlogger')

now = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))

def genMsg(msg:str or dict)->str:
    text = ''
    if type(msg) == dict:
        for item,item_val in msg.items():
            if type(item) == Stock:
                text += f'{item.name} {item}\n'
            else:   text += f'{item} \n'
            for k,v in item_val.items():
                text += f'  {k}： {v}\n'
    elif type(msg) == str:
        text += msg
    return text

def PushMessages(user:User, msg:dict() or str()):
    
    text = genMsg(msg)
    
    id = UserLineID.objects.get(user=user).line_id
    if not id:  return 
    try:
        line_bot_api.push_message(id,TextSendMessage(text=text))  
    except LineBotApiError as e:
        print(e)
        return
    
def getUserNews(user:User):
    msg = {}
    stock_list = user.sublist.stock_list.all()
    if stock_list:
        for stock in stock_list:
            news_list = News.objects.filter(related_stock=stock,).order_by('date_time')[:5]
            for news in news_list:
                if news.title in msg:   continue
                msg[news.title] = {
                    '時間'  :   news.date_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M"),
                    '原文網址'   :   news.url,
                }
    else:
        msg = '你的訂閱列表目前為空！'
    return msg
    
def getUserStock(user:User):
    msg = {}
    stock_list = user.sublist.stock_list.all()
    if stock_list:
        for stock in stock_list:
            cur_p = HistoryPrice.objects.filter(stock_code=stock).order_by('-date_time').first()
            if cur_p:
                open_p = HistoryPrice.objects.filter(stock_code=stock,date_time__date=cur_p.date_time.date(),).first()
                diff = cur_p.price-open_p.price
                diff_percent = str(round(diff/open_p.price*100,2)) + '%'
            else:
                open_p = '-'
                diff = '-'
                diff_percent = '-'
            msg[stock] = {
                '時間'  :   cur_p.date_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M") if cur_p else None,
                '現價'   :   cur_p.price,
                '開盤'  :   open_p.price,
                '漲跌'  :   diff,
                '漲跌%':   diff_percent,
            }
    else:
        msg = '你的訂閱列表目前為空！'
    return msg

def getUserStockSummary(user:User):
    msg = {}
    stock_list = user.sublist.stock_list.all()
    if stock_list:
        for stock in stock_list:
            stock_p = HistoryPriceSummary.objects.filter(stock=stock).order_by('-date').first()
            if stock_p:
                msg[stock] = {
                    '時間' : stock_p.date,
                    '高點' : stock_p.high,
                    '低點' : stock_p.low,
                    '開盤' : stock_p.open,
                    '收盤' : stock_p.close,
                    '漲跌' : stock_p.change,
                    '漲跌幅' : stock_p.change_p,
                
                }
            else:
                msg[stock] = {'錯誤': '暫無資料'}
    else:
        msg = '你的訂閱列表目前為空！'
    return msg

def pushNews(user_list=None):
    
    if not user_list:
        user_list = UserLineID.objects.all()
    try:
        iter(user_list)
    except TypeError:
        user_list = [user_list]
    finally:
        for user in user_list:
            if user.activate and user.pushNews and user.line_id:
                PushMessages(user.user,getUserNews(user.user))
        logger.info('Finished pushing news!')
    
        
def pushStock(user_list=None):
    
    if not user_list:
        user_list = UserLineID.objects.all()
    try:
        iter(user_list)
    except TypeError:
        user_list = [user_list]
    finally:
        for user in user_list:
            if user.activate and user.pushPrice and user.line_id:
                PushMessages(user.user,getUserStock(user.user))
        logger.info('Finished pushing stock!')
            
def pushStockSummary(user_list=None):
    if not user_list:
        user_list = UserLineID.objects.all()
    
    try:
        iter(user_list)
    except TypeError:
        user_list = [user_list]
    finally:
        for user in user_list:
            if user.activate and user.pushPrice and user.line_id:
                PushMessages(user.user,getUserStockSummary(user.user))
        logger.info('Finished pushing stock summary!')
            
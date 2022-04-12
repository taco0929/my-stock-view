from .setup import *
from django.core.exceptions import ObjectDoesNotExist
import datetime,pytz
from django.db.models import Q, QuerySet
from ..scripts import push_message
import logging
logger = logging.getLogger('testlogger')
from my_stock_view import settings

login_help = ''
command_list = (
            '登入',
            '登出',
            '最近新聞',
            '最近股價',
            '股票資訊',
            '我的新聞',
            '我的股價',
            '我的設定',
            '股價',
            '新聞',
            '主頁',
)
general_text ='可供選項：\n'
for i,v in enumerate(command_list):
    general_text+= f'{i+1}. {v}\n'
general_text += '輸入 \'help 選項\' 以查看詳細說明。'

usage_text = {
    'general' : general_text,
    '登入' : '1. 於網頁(https://my-stock-view.herokuapp.com/)註冊帳號\n2. 點擊左方欄位\'連結Line帳號\'\n3. 點擊產生驗證碼\n4. 直接回覆官方帳號驗證碼即可登入囉！',
    '登出' : '取消Line ID與my-stock-view的連結',
    '最近新聞':'將回傳10則最新新聞',
    '最近股價':'將隨機回傳5支股票的現價與開盤價',
    '股票資訊':'將回傳股票市場資訊\n輸入\'股票資訊 股票名字/代碼\'以進行查詢',
    '我的新聞':'(需登入)回傳訂閱的股票的相關新聞',
    '我的股價':'(需登入)回傳訂閱的股票的現價',
    '我的設定':'(需登入)回傳推送設定\n輸入\'我的設定 啟用功能/推送新聞/推送股價 開/關\' 以更改設定。',
    '股價':'可供查詢股票。\n輸入\'股價 股票名字/代碼\' 以查詢該股票的現價。',
    '新聞':'可供查詢新聞。\n輸入\'新聞 關鍵字\' 以進行查詢。',
    '主頁': '回傳主頁網址'
}

def cal_time_delta(time1, time2=None):
    if not time2:   time2 = datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE))
    d = time2 - time1
    return float(d.total_seconds())

def searchStock(q:str) -> QuerySet or str:
    stock = Stock.objects.filter(Q(name__icontains=q) | Q(code__icontains=q)| Q(sector__name__icontains=q))
    if len(stock) == 0:
        return '很抱歉，目前查無資料！'
    elif len(stock) == 1:
        return stock
    else:
        msg = '查詢到一個以上的資料！你是指...\n'
        for s in stock:
            msg += f'{s.name} {s.code}\n'
        return msg.strip()

class botResponse:
    def __init__(self,event:dict):
        self.event = event
        self.response = ''
        self.user = None   
        self.identify_user()
        
    def identify_user(self):
        try:
            self.user = UserLineID.objects.get(line_id=self.event.source.sender_id)
        except ObjectDoesNotExist as e:
            self.user = None

    
    def command_handler(self,command,**options) -> str():
        '''
        Use for handle field-changing commands.
        Expect:
            object: Model object
                Use for calling save()
            options: dict() {<name>:<model fields>}
                Contains name of fields for user to query, and the fields itself
            actions: dict() {<name>:<value>}
                Contains name of action for user to execute, and the value for changing the field
        Optional:
            'usage_text': str
                Return help text
        
        '''
        msg = ''
        if len(command) == 1:
            
            for k,v in options['options'].items():
                msg += f'{k}：{v}\n'
            return msg.strip()
        else:
            if command[1] == 'help':
                return options['usage_text'] if 'usage_text' in options else ''
                
            elif command[1] not in options['options']:
                msg += f'錯誤！選項{command[1]}不存在。可供選項：\n'
                [msg+f'{k}\n' for k in options['options']]
                return msg.strip()
            else:
                if len(command) == 2:
                    msg += command[1]+ '：' + options['options'][command[1]]
                    return msg
                else:
                    if command[2] not in options['actions']:
                        msg += f'錯誤！選項{command[2]}不存在。可供選項：\n'
                        [msg + f'{k}\n' for k in options['actions']]
                        return msg.strip()
                    else:
                        options['options'][command[1]] = options['actions'][command[2]]
                        options['object'].save()
                        msg += '設定完成！目前設定：\n'
                        for k,v in options['options'].items():
                            msg += f'{k}：{v}\n'
                            return msg.strip()
            
    
    def parse_msg(self,) -> str:
        '''
        Process input message.
        '''
        if self.event.message.type == 'text' and self.event.message.text:
            command = self.event.message.text.strip().split()
        else:   return usage_text['general']
        if command and UserLineID.objects.filter(token=command[0]):
            if UserLineID.objects.filter(token=command[0]).first().token_ini and 0 <= cal_time_delta(UserLineID.objects.filter(token=command[0]).first().token_ini) <= 300:
                u = UserLineID.objects.get(token=command[0])
                u.line_id = self.event.source.sender_id
                u.save()
                return '連結Line帳號成功！'
        elif command[0] not in command_list:  
            if command[0] == 'help':
                if len(command) == 1:   return usage_text['general']
                else:
                    return self.command_handler(command,options=usage_text)

            else:
                return usage_text['general']
        else:
            if command[0] == command_list[0]:   # 登入
                return usage_text['登入']
            
            elif command[0] == command_list[1]: # 登出
                if not self.user:    return '請先連結Line帳號'
                else:
                    self.user.line_id = None
                    return '登出成功！'
                
            elif command[0] == command_list[2]: # 最近新聞
                news_list = News.objects.all()[:10]
                msg = ''
                for news in news_list:
                    msg += f'{news.title}：\n  時間：{news.date_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M")}\n  原文網址：{news.url}\n'
                return msg
            
            elif command[0] == command_list[3]: # 最近股價
                stock_list = Stock.objects.order_by('?').all()[:5]
                cur_price_list = [HistoryPrice.objects.filter(stock_code=stock).last() for stock in stock_list]
                if not cur_price_list:
                    return '暫無資料...'
                open_price_list = [HistoryPrice.objects.filter(stock_code=p.stock_code,date_time__date=p.date_time.date()).first() for p in cur_price_list]
                msg = ''
                
                for i,stock in enumerate(stock_list):
                    msg+= f'{stock.name} {stock.code}\n'
                    msg+= f'  現價：{cur_price_list[i].price}\n  開盤：{open_price_list[i].price}\n  漲跌：{cur_price_list[i].price-open_price_list[i].price}\n  漲跌幅：{round((cur_price_list[i].price-open_price_list[i].price)/open_price_list[i].price*100,2)}  %\n'
                return msg
            elif command[0] == command_list[4]: # 股票資訊
                if len(command)==1:
                    return usage_text['股票資訊']   # return usage
                q = command[1]
                res = searchStock(q)
                if type(res) == str:    return res

                inf = StockInformation.objects.get(stock=res[0])
                msg = \
f'''\
{inf.stock.name} {inf.stock.code} {res[0].sector}
ROE： {inf.roe}
ROA： {inf.roa}
營收： {inf.revenue}
營收成長： {inf.revenue_growth}
營收/每股： {inf.revenue_per_share}\
'''
                
                return msg
            
            elif command[0] == command_list[5]: # 我的新聞
                if not self.user:    return '請先連結Line帳號'
                msg = push_message.getUserNews(self.user.user)
                logger.info(msg)
                return push_message.genMsg(msg)
            
            elif command[0] == command_list[6]: # 我的股價
                if not self.user:    return '請先連結Line帳號'
                msg = push_message.getUserStock(self.user.user)
                return push_message.genMsg(msg)
            
            elif command[0] == command_list[7]: # 我的設定
                if not self.user:    return '請先連結Line帳號'
                return self.command_handler(
                    command,
                    command_type='setting',
                    object=self.user,
                    options = {
                        '啟用功能' : self.user.activate,
                        '推送新聞' : self.user.pushNews,
                        '推送股價' : self.user.pushPrice,
                    },
                    actions = {
                        '開' : True,
                        '關' : False,
                        }
                    )

            elif command[0] == command_list[8]: # 股價
                if len(command) == 1:
                    return  usage_text['股價']  # Usage text
                q = command[1]
                res = searchStock(q)
                if type(res) == str:
                    return res
                cur_price = HistoryPrice.objects.filter(stock_code=res[0]).order_by('-date_time').first() or '-'
                
                open_price = '-'
                d = '-'
                diff = '-'
                diff_p = '-'
                if type(cur_price) != str:
                    cur_price = cur_price.price
                    d = cur_price.date_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M")
                    open_price = HistoryPrice.objects.filter(stock_code=res[0],date_time__date=cur_price.date_time.date()).first().price
                    diff = cur_price.price - open_price
                    diff_p = round(diff/open_price*100,2)
                msg = f'{res[0].name} {res[0].code}\n時間：{d}\n現價：{cur_price}\n開盤：{open_price}\n漲幅：{diff}\n漲幅% ：{diff_p}'
                return msg
            
            elif command[0] == command_list[9]: # 新聞
                if len(command) == 1:
                    return usage_text['新聞']   # Usage text
                q= command[1]
                news_list = News.objects.filter(Q(title__icontains=q) | Q(related_stock=q)).order_by('-date_time')[:10]
                msg = f'搜尋{q}結果為：\n'
                if news_list:
                    for news in news_list:
                        msg += f'{news.title}\n時間：{news.date_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.TIME_ZONE)).strftime("%Y-%m-%d %H:%M")}\n原文網址：{news.url}\n內文：{news.content}\n'
                else:
                    msg+='查無結果...'
                return msg.strip()
            
            elif command[0] == command_list[10]: # 主頁
                return '主頁網址：https://my-stock-view.herokuapp.com/'
        
                
                    
                
        
            
        
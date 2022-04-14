from django.test import TestCase
from catalog.models import *
import logging
logger = logging.getLogger('testlogger')
from linebot.models.events import MessageEvent
# Create your tests here.
import datetime
import pytz
from my_stock_view import settings

from mylinebot.scripts.bot_response import botResponse,command_list

class LineBotTest(TestCase):
    def setUp(self):
        u,created = User.objects.get_or_create(username='user1')
        UserLineID.objects.create(user=u,line_id='test123')
        Sector.objects.create(name='半導體')
        tsmc = Stock.objects.create(name='台積',code='23300',sector=Sector.objects.get(name='半導體'))
        s_inf = StockInformation.objects.get(stock=tsmc,)
        s_inf.business_describ='護國神山'
        s_inf.save()
        n = News.objects.create(title='測試新聞',date_time=datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)))
        n.related_stock.add(tsmc)
        s = SubList.objects.create(username=u,)
        s.stock_list.add(tsmc)
        for i in range(5):
            s = HistoryPrice.objects.create(stock_code=tsmc,date_time=datetime.datetime(2022,4,1,datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).hour,i+1,0,tzinfo=pytz.timezone(settings.TIME_ZONE)),price=(i+10)*10)
            logger.info(s.date_time.replace(tzinfo=pytz.utc).astimezone(pytz.timezone(settings.TIME_ZONE)))
            
        
    def create_webhook(self,input=None,userID=None):
        
        e ={
                "type" : "message",
                "message" : {
                    "type" : "text",
                    "id" : "1234567",
                    "text" : input or "hello world",
                },
                "source": {
                    "type": "user",
                    "userId": userID or "test123"
                },
            }
        # event = json.dumps(e)
        msg = MessageEvent.new_from_json_dict(e)
        
        return msg
    
    def test_recieve_msg(self,input='股價 2330'):
        r = botResponse(self.create_webhook(input))
        msg = r.parse_msg()
        logger.info(msg)
        
    def test_commands(self):
        for command in command_list:
            if command =='登出': continue
            r = botResponse(self.create_webhook(input=command))
            logger.info(command)
            logger.info(r.parse_msg())
    
    def test_help(self):
        for command in command_list:
            r = botResponse(self.create_webhook(input='help ' + command))
            logger.info('help ' + command)
            logger.info(r.parse_msg())

class test_verify(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='user1')
        self.user_line = UserLineID.objects.create(user=self.user,line_id='userid',token='asdf',token_ini=datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)))
        
    def create_webhook(self,input=None,userID=None):
    
        e ={
                "type" : "message",
                "message" : {
                    "type" : "text",
                    "id" : "1234567",
                    "text" : input or "hello world",
                },
                "source": {
                    "type": "user",
                    "userId": userID or "test123"
                },
            }
        # event = json.dumps(e)
        msg = MessageEvent.new_from_json_dict(e)
        
        return msg

    def testVerify(self):
        # Connect
        r = botResponse(self.create_webhook(input='asdf',userID='userid'))
        logger.info(r.parse_msg())
        
        # Check setting
        r = botResponse(self.create_webhook(input='我的設定',userID='userid'))
        logger.info(r.parse_msg())
        
        # Check changing setting
        r = botResponse(self.create_webhook(input='我的設定 啟用功能 關',userID='userid'))
        logger.info(r.parse_msg())
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from my_stock_view import settings
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

from mylinebot.scripts import bot_response
import logging
logger = logging.getLogger('testlogger')
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

 
@csrf_exempt
def callback(request):
    logger.info('Start callback...')
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            logger.info(event)
            try:
                if isinstance(event, MessageEvent):  # 如果有訊息事件
                    r = bot_response.botResponse(event)
                    msg = r.parse_msg()
                    logger.info(msg)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=msg)
                    )
            except Exception as e:
                logger.error(e.with_traceback())
                return HttpResponseBadRequest()
        return HttpResponse()
    else:
        
        return HttpResponseBadRequest()
from linebot import LineBotApi
from linebot.exceptions import LineBotApiError
from my_stock_view.settings import LINE_CHANNEL_ACCESS_TOKEN
from my_stock_view import settings
from catalog.models import *

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

from django.test import TestCase
from catalog.models import *
from .scripts.crawler_functions import *
import logging
logger = logging.getLogger('testlogger')
# Create your tests here.


class CrawlTest(TestCase):
    def setUp(self):
        self.sector = Sector.objects.create(name='半導體')
        self.stock = Stock.objects.create(name='台積電',code='2330',sector=self.sector)
    
    def test_crawl(self):
        get_stock_information(self.stock)
        logger.info(StockInformation.objects.get(stock=self.stock).roe)
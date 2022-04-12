from django.core.management.base import BaseCommand
from crawler.scripts.news_crawler import *
from crawler.scripts.crawler_functions import *
import datetime
import pytz
from  my_stock_view import settings

class Command(BaseCommand):
    def add_arguments(self, parser) -> None:
        parser.add_argument('crawl_object',metavar='news | stock | stock_sum',type=str,nargs='+')
        
    def handle(self, *args, **options):
        if not options['crawl_object']:
            self.stdout.write(self.style.ERROR('Missing argument: news|stock|stock_sum'))
        for crawl_object in options['crawl_object']:
            if crawl_object:
                
                if type(crawl_object) != str:
                    self.stdout.write(self.style.ERROR( f'Invalid argument: {crawl_object} Expecting sting\n Options: news|stock|stock_sum'))
                    continue
                crawl_object = crawl_object.lower()
            if crawl_object!= 'news' and crawl_object!='stock' and crawl_object!='stock_sum':
                self.stdout.write(self.style.ERROR( f'Invalid argument: {crawl_object}\n Options: news|stock|stock_sum'))
                continue
            if crawl_object == 'news':
                get_news()
                self.stdout.write(self.style.SUCCESS('Finished crawling news.'))
            elif crawl_object == 'stock':
                if (datetime.date.today().isoweekday()==6 or datetime.date.today().isoweekday()==7) or datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).hour > 14 or datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).hour < 9:
                    continue
                get_stock_cur_price()
                self.stdout.write(self.style.SUCCESS('Finished crawling current stock price.'))
                
            elif crawl_object == 'stock_sum':
                if datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).hour > 14 or datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).hour < 9:
                    continue
                update_exist_stock_hp_sum()
                self.stdout.write(self.style.SUCCESS('Finished crawling stock price summary.'))
        
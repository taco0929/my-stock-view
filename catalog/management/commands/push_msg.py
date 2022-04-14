from django.core.management.base import BaseCommand,CommandParser
from mylinebot.scripts import push_message
import datetime
import pytz
from my_stock_view import settings


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('push_obj',metavar='news | stock | stock_sum',type=str, nargs='+')
        
    def handle(self,*args, **options):
        if not options['push_obj']:
            self.stdout.write(self.style.ERROR('Missing argument: news|stock|stock_sum'))
        for push_obj in options['push_obj']:
            if push_obj:
                
                if type(push_obj) != str:
                    self.stdout.write(self.style.ERROR( f'Invalid argument: {push_obj} Expecting sting\n Options: news|stock|stock_sum'))
                    continue
                
            if push_obj!= 'news' and push_obj!='stock' and push_obj!='stock_sum':
                self.stdout.write(self.style.ERROR( f'Invalid argument: {push_obj}\n Options: news|stock|stock_sum'))
                continue
            if push_obj == 'news':
                push_message.pushNews()
                self.stdout.write(self.style.SUCCESS('Finished pushing news.'))
            elif push_obj == 'stock':
                if (datetime.date.today().isoweekday()==6 or datetime.date.today().isoweekday()==7) or datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).hour > 14 or datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).hour < 9:
                    continue
                push_message.pushStock()
                self.stdout.write(self.style.SUCCESS('Finished pushing Stocks.'))
            elif push_obj == 'stock_sum':
                if datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).hour > 14 or datetime.datetime.now(tz=pytz.timezone(settings.TIME_ZONE)).hour < 9:
                    continue
                push_message.pushStockSummary()
                self.stdout.write(self.style.SUCCESS('Finished pushing Stock Summary.'))
            
from django.core.management.base import BaseCommand
from crawler.scripts.db_control import *

class Command(BaseCommand):
    help = 'Controls database size and delete old data'
    
    def handle(self,*args, **options):
        news_ctrl()
        hp_ctrl()
        hp_sum_ctrl()
        
        self.stdout.write(self.style.SUCCESS('Database management done.'))
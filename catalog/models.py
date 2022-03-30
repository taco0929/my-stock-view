from django.db import models
from datetime import datetime

# Create your models here.

from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import User
import datetime


class Sector(models.Model):
    name = models.CharField(max_length=20, help_text="Enter the name of the sector", primary_key=True)
    
    def __str__(self):
        '''
        Return the name of the sector
        '''
        return self.name
    
    def get_absolute_url(self):
        return reverse("sector-list", args=[str(self.name)])

class Stock(models.Model):
    name = models.CharField(max_length=20, help_text='Enter name of the stock',blank=False)
    code = models.CharField(max_length=10, help_text='Enter code of the stock', blank=False, primary_key=True)
    sector = models.ForeignKey(Sector, on_delete=models.SET_NULL,null=True)
    
    
    def __str__(self):
        '''
        Return the the code of the stock
        '''
        return self.code
    
    def get_absolute_url(self):
        return reverse("stock-code", args=[str(self.code)])
    
    #def get_last_open_price(self):
        
    #def get_last_price(self):

 


class StockInformation(models.Model):
    stock = models.OneToOneField(Stock,on_delete=models.CASCADE,primary_key=True)
    business_describ = models.TextField(help_text='Enter the describtion of the corps.',null=True,blank=True)    
    market_value = models.IntegerField(help_text='Enter the market value of the corps',null=True,blank=True)

    def __str__(self):
        return self.stock.code

    
class News(models.Model):
    title = models.CharField(max_length=100,help_text='Enter the title of the news',primary_key=True)
    url=models.URLField(max_length=255,null=True,blank=True)
    content = models.TextField(help_text='Enter the content of the news', null=True, blank=True)
    date_time = models.DateTimeField(default=datetime.datetime.now)
    related_stock = models.ManyToManyField(Stock,null=True, blank=True)
    
    def display_related_stock(self):
        return ', '.join(stock.code for stock in self.related_stock.all()[:3])
    
    class Meta:
        ordering = ['date_time']

    

class HistoryPrice(models.Model):
    stock_code = models.ForeignKey(Stock,on_delete=models.SET_NULL,null=True)
    date_time = models.DateTimeField(db_index=True,)
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    
    
    def __str__(self):
        '''Return information of the stock'''
        return f'{self.stock_code.code} {self.date_time} {self.price}'
    
    def get_latest_datetime(self,stock_code):            
        latest = HistoryPrice.objects.order_by('date_time').filter(stock_code__code=stock_code).exclude(price=None).values()
        if not latest:  return None
        return latest.last()['date_time'].strftime('%Y-%m-%d %H:%M:%S')
    def get_latest_price(self,stock_code):
        latest = HistoryPrice.objects.order_by('date_time').filter(stock_code__code=stock_code).exclude(price=None).values()
        if not latest:  return None
        return str(latest.last()['price'])
    

    def get_open_price(self,stock_code):
        open = HistoryPrice.objects.order_by('date_time').filter(stock_code__code=stock_code,date_time__date=datetime.date.today(),date_time__time='09:00:00').exclude(price=None).values()
        if not open:    return None
        return str(open.last()['price'])
    
    def get_today_high(self,stock_code):
        high = HistoryPrice.objects.order_by('date_time__date','price').filter(stock_code__code=stock_code,date_time__date=datetime.date.today()).exclude(price=None).values()
        if not high:    
            return None
        return str(high.last()['price'])
    def get_today_low(self,stock_code):
        low = HistoryPrice.objects.order_by('date_time__date','price').filter(stock_code__code=stock_code,date_time__time=datetime.date.today()).exclude(price=None).values().first()
        return str(low.last()['price'])
    
    class Meta:
        ordering = ['stock_code','date_time']
        
  
class SubList(models.Model):
    username = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    stock_list = models.ManyToManyField(Stock,null=True,blank=True)

    def __str__(self):
        return self.username.username
    

    
        
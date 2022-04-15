from django.db import models
from datetime import datetime

# Create your models here.

from django.urls import reverse,reverse_lazy
from django.contrib.auth.models import User
import datetime
from my_stock_view.settings import get_hash

class UserLineID(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    line_id = models.CharField(max_length=63,blank=True,default=None,null=True)
    activate = models.BooleanField(default=True)
    pushNews = models.BooleanField(default=True)
    pushPrice = models.BooleanField(default=True)
    token = models.CharField(max_length=6,null=True,blank=True)
    token_ini = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.user.username


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
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE,null=True)
    
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        inf = StockInformation(stock=self)
        inf.save()
        
        
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
    market_value = models.BigIntegerField(help_text='Enter the market value of the corps',null=True,blank=True)
    roe = models.DecimalField(max_digits=20,decimal_places=4,null=True,blank=True)
    roa = models.DecimalField(max_digits=20,decimal_places=4,null=True,blank=True)
    revenue = models.BigIntegerField(null=True,blank=True)
    revenue_growth = models.DecimalField(max_digits=20,decimal_places=4,null=True,blank=True)
    revenue_per_share = models.DecimalField(max_digits=20,decimal_places=4,null=True,blank=True)

    def __str__(self):
        return self.stock.code

    
class News(models.Model):
    title = models.CharField(max_length=128,help_text='Enter the title of the news')
    url=models.TextField(max_length=255,null=True,blank=True)
    content = models.TextField(help_text='Enter the content of the news', null=True, blank=True)
    date_time = models.DateTimeField(default=datetime.datetime.now)
    related_stock = models.ManyToManyField(Stock, blank=True)
    
    def display_related_stock(self):
        return ', '.join(stock.code for stock in self.related_stock.all()[:3])
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-date_time']

    

class HistoryPrice(models.Model):
    stock_code = models.ForeignKey(Stock,on_delete=models.CASCADE,null=True)
    date_time = models.DateTimeField(db_index=True,help_text='default timezone:UTF')
    price = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    
    def __str__(self):
        '''Return information of the stock'''
        return f'{self.stock_code.code} {self.date_time} {self.price}'
    
    class Meta:
        ordering = ['stock_code','date_time']
        
  
class SubList(models.Model):
    username = models.OneToOneField(User,primary_key=True,on_delete=models.CASCADE)
    stock_list = models.ManyToManyField(Stock,blank=True)

    def __str__(self):
        return self.username.username
    
class HistoryPriceSummary(models.Model):
    stock = models.ForeignKey(Stock,on_delete=models.CASCADE,null=True)
    date = models.DateField(db_index=True)
    high = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    low = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    open = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    close = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    change = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    change_p = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    
    
    
    def __str__(self):
        return self.stock.code
    
    def save(self,*args,**kwargs):
        if self.open and self.close:
            self.change = self.close-self.open
            self.change_p = (self.close-self.open)/self.open*100
        super().save(*args,**kwargs)
    
    class Meta:
        ordering = ['stock','-date']
    
        
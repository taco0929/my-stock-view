from django.shortcuts import render, redirect

# Create your views here.

from django.views import generic
from django.views.generic.edit import CreateView
from .models import HistoryPrice, News, Sector,Stock, StockInformation
from django.db.models import Q
import datetime
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
import random

def index(request):
    '''View function for home page of the site'''
    context = {}
    latest_news = News.objects.order_by('-date_time').all().distinct()
    if latest_news.count() > 10:    latest_news=latest_news[:10]
    context.update({
        'latest_news'           :   latest_news,
        })
    random_stock_list = Stock.objects.all().order_by('?')[:10]
    stock_list_price = {}
    for stock in random_stock_list:
        stock_list_price[stock] = [
            HistoryPrice().get_open_price(stock),
            HistoryPrice().get_latest_price(stock)
        ]
        if HistoryPrice().get_open_price(stock) and HistoryPrice().get_latest_price(stock):
            stock_list_price[stock].append(f'{round((float(HistoryPrice().get_latest_price(stock))-float(HistoryPrice().get_open_price(stock)))/float(HistoryPrice().get_open_price(stock)),2)}%')
        else:   stock_list_price[stock].append('-')
    context.update({
        'random_stock_list'     :   random_stock_list,
        'stock_price_list'      :   stock_list_price,
    })
    
    
    return render(request, 'index.html',context)

class SectorListView(generic.ListView):
    model = Sector
    

    
'''
class StockDetailView(generic.DetailView):
    model = Stock
    
    history_price = HistoryPrice()
    open = history_price.get_open_price()
 '''
        
 
def StockDetailView(request,pk):
    stock = Stock.objects.filter(code=pk).values()[0]
    stock_name = stock['name']
    sector = stock['sector_id']
    
    hisory_price = HistoryPrice()
    open = hisory_price.get_open_price(pk)
    latest = hisory_price.get_latest_price(pk)
    changes=round(float(latest)-float(open),2) if open else '-'
    
    changes_percent = f'{round(float(changes)/float(open),2)}%' if open else '-'
    
    today_price = HistoryPrice.objects.filter(stock_code=pk,date_time__date=datetime.date.today()).order_by('-date_time')
    if len(today_price) > 10:    today_price= today_price[:10]
    
    news = News.objects.filter(related_stock=pk)
    if len(news) > 10:  news = news[:10]
    
    stock_inf = StockInformation.objects.filter(stock=pk).values()
    if stock_inf:   stock_inf = stock_inf[0]

    
    context = {
        'stock'               :   stock,
        
        'today_price'         :   today_price,
        
        'open'                :   open,
        'latest'              :   latest,
        'changes'             :   changes,
        'changes_percent'     :   changes_percent,
        
        'news'                :   news,
        
        'stock_inf'           :   stock_inf,
        

    }
    return render(request,'./catalog/stock_detail.html',context=context)
     
    
class NewsListView(generic.ListView):
    model = News
    

class NewsDetailView(generic.DetailView):
    model = News
    
def HistoryPriceDetailView(request,pk):
    stock_price_list = HistoryPrice.objects.filter(stock_code__code=pk).order_by('-date_time')
    stock = Stock.objects.filter(code=pk).first()
    context = {
        'stock'             :   stock,
        'stock_price_list'  :   stock_price_list,
    }
    paginator = Paginator(stock_price_list,25)
    page_number=request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context.update({
        'page_obj'  :   page_obj,
    })
    return render(request,'./catalog/history_price.html',context=context)


from django.contrib import messages

def search_stock(request):
    q = request.GET.get('q')
    if not q:   q = ''
    stock = Stock.objects.filter(Q(name__icontains=q) | Q(code__icontains=q)| Q(sector__name__icontains=q)).distinct().order_by('code')
    paginator = Paginator(stock,15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'./catalog/search_stock.html',{'stock':stock,'page_obj':page_obj,'q':q})

def search_news(request):
    q = request.GET.get('q')
    
    if not q:
        news = News.objects.order_by('-date_time').distinct()
        paginator = Paginator(news,15)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request,'./catalog/search_news.html',{'news':news,'page_obj':page_obj,'q':q,})
    
    news = News.objects.filter(Q(title__icontains=q)|Q(related_stock__code=q)|Q(related_stock__name__icontains=q)).order_by('-date_time').distinct()
    paginator = Paginator(news,15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'./catalog/search_news.html',{'news':news,'page_obj':page_obj,'q':q,})
    






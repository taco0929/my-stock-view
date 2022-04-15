from django.shortcuts import render, redirect

# Create your views here.

from django.views import generic
from django.views.generic.edit import CreateView
from .models import HistoryPriceSummary, HistoryPrice, News, Sector,Stock, StockInformation
from django.db.models import Q
import datetime
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login

def index(request):
    '''View function for home page of the site'''
    context = {}
    latest_news = News.objects.order_by('-date_time').all().distinct()
    if latest_news.count() > 10:    latest_news=latest_news[:10]
    context.update({
        'latest_news'           :   latest_news,
        })
    random_stock_list = Stock.objects.all().order_by('?')[:10]
    price_list = [HistoryPriceSummary.objects.filter(stock=i).last() for i in random_stock_list]
    
    context.update({
        'random_stock_list'     :   random_stock_list,
        'price_list'            :   price_list,
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
    stock = Stock.objects.get(code=pk)
    inf = StockInformation.objects.get(stock=stock)
    
    h_inf =  HistoryPriceSummary.objects.filter(stock=stock).order_by('date').last()
    latest_p = HistoryPrice.objects.filter(stock_code=stock).last().price if HistoryPrice.objects.filter(stock_code=stock).last() else  HistoryPriceSummary.objects.filter(stock=stock).last().close
    open_p = HistoryPrice.objects.filter(stock_code=stock).first().price if HistoryPrice.objects.filter(stock_code=stock).first() else HistoryPriceSummary.objects.filter(stock=stock).first().open
    today_p = HistoryPrice.objects.filter(stock_code=stock,date_time__date=datetime.date.today()).order_by('-date_time')[:10] or HistoryPrice.objects.filter(stock_code=stock,date_time__date=h_inf.date).order_by('-date_time')[:10]
    change = (latest_p - open_p) if (latest_p) else '-'
    change_p = round(change / open_p,2) if open_p else '-'
    news_list = News.objects.filter(related_stock=stock)[:10]

    context = {
        'stock'     :       stock,
        'inf'       :       inf,
        'h_inf'     :       h_inf,
        'latest_p'  :       latest_p,
        'open_p'    :       open_p,
        'today_p'   :       today_p,
        'change'    :       change,
        'change_p'  :       change_p,
        'news'      :       news_list,
    }
    return render(request,'./catalog/stock_detail.html',context=context)
     
    
class NewsListView(generic.ListView):
    model = News
    

class NewsDetailView(generic.DetailView):
    model = News
    
def HistoryPriceDetailView(request,pk):
    stock_price_list = HistoryPrice.objects.filter(stock_code__code=pk).order_by('-date_time')
    
    stock = Stock.objects.get(code=pk)
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

def HistoryPriceSummaryDetailView(request,pk):
    stock_price_list = HistoryPriceSummary.objects.filter(stock__code=pk).order_by('-date')
    
    stock = Stock.objects.get(code=pk)
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
    return render(request,'./catalog/history_price_summary.html',context=context)


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
    
    news = News.objects.filter(Q(id__icontains=q)|Q(related_stock__code=q)|Q(related_stock__name__icontains=q)|Q(title__icontains=q)).order_by('-date_time').distinct()
    paginator = Paginator(news,15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'./catalog/search_news.html',{'news':news,'page_obj':page_obj,'q':q,})
    






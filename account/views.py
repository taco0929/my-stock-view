from django.shortcuts import render,redirect

# Create your views here.

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import user_passes_test,login_required
from catalog.models import HistoryPrice, SubList,Stock, UserLineID
from django.views import generic
from django.core.paginator import Paginator
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
import datetime
import pytz
from my_stock_view.settings import TIME_ZONE

@user_passes_test(lambda u: not u.is_authenticated)
def SignUpView(request):
    
    if request.method == 'POST': 
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, './registration/sign_up.html', {'form': form})


    
@login_required 
def UserSubList(request):
    user = request.user
    stock_list = user.sublist.stock_list.all()
    
    stock_price_list = {}
    for stock in stock_list:
        tmp = HistoryPrice.objects.filter(stock_code=stock).last()
        if tmp: tmp = tmp.date_time.date()
            
        stock_price_list[stock] = (
            HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).first().price if HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).first() else None,
            HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).last().price if HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).first() else None,
            HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).last().price - HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).first().price if HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).first() else None,
                )
        
    stock_price_list = tuple(stock_price_list.items())
    
    paginator = Paginator(stock_price_list,25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {

        'stock_list'        :   stock_list,
        'page_obj'          :   page_obj,
        'stock_price_list'  :   stock_price_list,
    }
    
    return render(request,'./user_page/sublist_user.html',context=context)
    
    
from .form import SubListItemUpdateForm, SublistItemDeleteForm, UserLineIdUpdateForm
from django.core.exceptions import ObjectDoesNotExist

def DeleteSubItem(request,pk):
    if request.user.is_authenticated:
        user = request.user
        stock_list = user.sublist.stock_list.all()
        form = SublistItemDeleteForm(instance=user.sublist)
        msg=''
        try:
            d = user.sublist.stock_list.get(code=pk)
        except ObjectDoesNotExist:
            d = ''
        if stock_list.filter(code=pk):
            if request.method == 'POST':
                user.sublist.stock_list.remove(user.sublist.stock_list.get(code=pk))
                return redirect('account:sublist')
        else:
            msg = f'錯誤！列表中無指定對象（{pk}）'
        

        context = {
            'form'  :   form,
            'msg'   :   msg,
            'd'     :   d,
        }
        return render(request,'./form/delete_form.html',context=context)
    else:        

        return redirect('login')

# http://localhost:8000/account/sublist/delete/0001/

from catalog.models import SubList, News, UserLineID

def UserMainPage(request,):
    if request.user.is_authenticated:
        user = request.user
        try:
            sublist = SubList.objects.get(username = user)
        except ObjectDoesNotExist:
            sublist = SubList(username=user)
            sublist.save()
        try:
            user_line = UserLineID.objects.get(user=user)
        except ObjectDoesNotExist:
            user_line = UserLineID(user=user)
            user_line.save()
        news_list = []
        
        for news in News.objects.all().order_by('-date_time'):
            if len(news_list)==5:   break
            if news.related_stock.all():
                for n in news.related_stock.all():
                    if n in sublist.stock_list.all():
                        news_list.append(news)
                        break

        stock_list = {}
        for stock in sublist.stock_list.all()[:5]:
            tmp = HistoryPrice.objects.filter(stock_code=stock).last()
            if tmp: tmp = tmp.date_time.date()
               
            stock_list[stock] = (
                HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).first().price if HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).first() else None,
                HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).last().price if HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).first() else None,
                HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).last().price-HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).first().price if HistoryPrice.objects.filter(stock_code=stock,date_time__date=tmp).first() else None)

        context = {
            
            'news_list' :   news_list,
            'stock_list':   stock_list,
            'sublist'   :   sublist,
        }
        return render(request,'./user_page/mainpage_user.html',context=context)
    
    
    else:
        return redirect('login')

from catalog.models import Stock

def AddSubItem(request,pk):
    if request.user.is_authenticated:
        user = request.user
        sub_list = user.sublist
        form = SubListItemUpdateForm(instance=user.sublist)
        msg=''
        item = Stock.objects.get(code=pk)
        if request.method == 'POST':
            
            item = Stock.objects.get(code=pk)
            if item in sub_list.stock_list.all():
                msg = '該股票已經在列表中！'
                
            else:   
                sub_list.stock_list.add(item)
                return redirect('stock-detail',pk)
        
        context = {
            'form'  :   form,
            'msg'   :   msg,
            'pk'    :   pk,
        }
        return render(request,'./form/add_form.html',context=context)
    else:        

        return redirect('login')

import random, string  
def ConnectLine(request):
    if request.user.is_authenticated:

        user_line = request.user.userlineid
        form = UserLineIdUpdateForm(instance=user_line)
        
        if request.method == 'POST':
            if request.POST.get('input_lineID',None):
                u = UserLineID.objects.get(user=request.user)
                token = ''.join(random.choice((string.ascii_lowercase+string.digits)) for _ in range(6))
                timestamp = datetime.datetime.now(tz=pytz.timezone(TIME_ZONE))
                u.token = token
                u.token_ini = timestamp
                u.save()
                return render(request,'registration/connect_to_line.html',context = {'msg':'請於官方帳號輸入驗證碼！', 'token' : token})
            elif request.POST.get('cancel'):
                u = UserLineID.objects.get(user=request.user)
                u.line_id = None
                u.save()
                msg = '已取消連結！'
                return render(request,'registration/connect_to_line.html',context = {'msg':msg})

        else:
            form = UserLineIdUpdateForm()
            return render(request,'registration/connect_to_line.html',context = {'form':form})
        
    else:
        return redirect('login')
    

            


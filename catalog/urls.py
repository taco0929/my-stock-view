
from unicodedata import name
from django.urls import path,include
from catalog import views
from account import views as account_views
urlpatterns = []

urlpatterns += [
    path('', views.index, name='index'),
]

urlpatterns += [
    path('sectors/',views.SectorListView.as_view(),name='sector-list')
]

urlpatterns += [
    path('stocks/<str:pk>/',views.StockDetailView,name='stock-detail'),
    path('stocks/<str:pk>/add/',account_views.AddSubItem,name='stock-detail-add'),
    path('news/<str:pk>/',views.NewsDetailView.as_view(),name='news-content'),
    path('stocks/<str:pk>/history_price/', views.HistoryPriceDetailView, name='history-price'),

]

urlpatterns += [
    
    path('search/stock/',views.search_stock,name='search-stock'),
    path('search/news/',views.search_news,name='search-news')
    
]

    


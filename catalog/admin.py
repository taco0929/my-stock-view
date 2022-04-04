from django.contrib import admin

# Register your models here.

from .models import Stock, Sector, News,StockInformation , HistoryPrice, SubList, HistoryPriceSummary

# admin.site.register(Stock)
admin.site.register(Sector)
# admin.site.register(News)
# admin.site.register(StockInformation)

#admin.site.register(HistoryPrice)
admin.site.register(SubList)

@admin.register(HistoryPrice)
class HistoryPriceAdmin(admin.ModelAdmin):
    list_display = ['stock_code','date_time','price']
    list_filter = ('date_time',)
    search_fields = ['stock_code__code','stock_code__name','stock_code__sector__name','date_time__date','date_time__time']
    

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['date_time','title','display_related_stock']
    list_filter = ('date_time',)
    search_fields = ['title','related_stock__code','related_stock__name']
    
    
@admin.register(StockInformation)
class StockInformationAdmin(admin.ModelAdmin):
    search_fields = ['stock__code','stock__name']
    
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    search_fields = ['name','code']

@admin.register(HistoryPriceSummary) 
class HisSumAdmin(admin.ModelAdmin):
    list_display = ['date', 'stock','open','close','high','low']
    search_fields = ['stock']
    list_filter = ['date']
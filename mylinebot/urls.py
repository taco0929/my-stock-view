from django.urls import path
from mylinebot import views 

urlpatterns = [
    path('callback/',views.callback),
]

from django.urls import path,include

from account import views
from django.contrib.auth import views as auth_views
app_name = 'account'


urlpatterns = []

urlpatterns += [
    path('signup/',views.SignUpView,name='sign-up'),
    path('sublist/',views.UserSubList,name='sublist'),
]

urlpatterns += [
    path('sublist/delete/<str:pk>/',views.DeleteSubItem,name='delete-item'),
    path('',views.UserMainPage,name='user-main')
]

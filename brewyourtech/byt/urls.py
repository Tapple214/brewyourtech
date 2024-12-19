from django.urls import path

from . import views

# To access on browser eg. path('login', views.login, name='login') > /login will show template in views.login

urlpatterns = [
    path('login', views.login, name='login'), 
    path('', views.brewLog, name='brewLog'),
    path('brewery', views.brewery, name='brewery'),
]
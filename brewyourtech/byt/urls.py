from django.urls import path

from . import views

urlpatterns = [
    path('navbar', views.navbar, name='navbar'),
    path('login', views.login, name='login'),
    path('', views.brewLog, name='brewLog'),
    path('brewery', views.brewery, name='brewery'),
]
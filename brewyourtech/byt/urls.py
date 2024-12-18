from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('', views.brewLog, name='brewLog'),
    path('brewery', views.brewery, name='brewery'),
]
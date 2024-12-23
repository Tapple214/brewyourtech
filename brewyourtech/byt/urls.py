### START ###

from django.urls import path
from rest_framework.routers import DefaultRouter
from .api import ToggleBookmarkView, PhoneBrewView, LaptopBrewView, CameraBrewView, TabletBrewView, BrewLogView
from django.contrib import admin
from . import views

urlpatterns = [
    path('main/', views.mainPage, name='main'),
    path('admin/', admin.site.urls),
    path('logout/', views.logout, name='logout'),
    path('brewery/', views.brewery, name='brewery'),
    path('loginSignUp/', views.loginSignUp, name='loginSignUp'),
    path('brewDisplay/<str:device_type>/<int:device_id>/<int:user_id>', views.brewDisplay, name='brewDisplay'),

    path('', BrewLogView.as_view(), name='brewLog'), 
    path('phoneBrew/', PhoneBrewView.as_view(), name='phoneBrew'),  
    path('laptopBrew/', LaptopBrewView.as_view(), name='laptopBrew'), 
    path('cameraBrew/', CameraBrewView.as_view(), name='cameraBrew'),  
    path('tabletBrew/', TabletBrewView.as_view(), name='tabletBrew'),
    path('api/toggle_bookmark/', ToggleBookmarkView.as_view(), name='toggle_bookmark'),
]

### END ###
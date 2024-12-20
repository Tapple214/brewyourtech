from django.urls import path

from . import views

# To access on browser eg. path('loginSignUp', views.loginSignUp, name='loginSignUp') > /login will show template in views.login

urlpatterns = [
    path('loginSignUp', views.loginSignUp, name='loginSignUp'), 
    path('', views.brewLog, name='brewLog'),
    path('brewery', views.brewery, name='brewery'),
    path('phoneBrew', views.phoneBrew, name='phoneBrew'),
    path('laptopBrew', views.laptopBrew, name='laptopBrew'),
    path('cameraBrew', views.cameraBrew, name='cameraBrew'),
    path('tabletBrew', views.tabletBrew, name='tabletBrew'),
    path('brewDisplay', views.brewDisplay, name='brewDisplay'),
]
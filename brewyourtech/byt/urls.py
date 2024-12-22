from django.urls import path

from . import views

# To access on browser eg. path('loginSignUp', views.loginSignUp, name='loginSignUp') > /login will show template in views.login

urlpatterns = [
    path('loginSignUp/', views.loginSignUp, name='loginSignUp'), 
    path('', views.brewLog, name='brewLog'),
    path('brewery/', views.brewery, name='brewery'),
    path('phoneBrew/', views.phoneBrew, name='phoneBrew'),
    path('laptopBrew/', views.laptopBrew, name='laptopBrew'),
    path('cameraBrew/', views.cameraBrew, name='cameraBrew'),
    path('tabletBrew/', views.tabletBrew, name='tabletBrew'),
    path('brewDisplay/<str:device_type>/<int:device_id>/<int:user_id>', views.brewDisplay, name='brewDisplay'),
    path("toggle_bookmark", views.toggle_bookmark, name="toggle_bookmark"), #api call
]
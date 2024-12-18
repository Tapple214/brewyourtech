from django.shortcuts import render

from .models import *

# Create your views here.

# Index/Home page aka "Brew Log"
def brewLog(request):
    response_string = User.objects.all()[0]
    return render(request, 'byt/brewLog.html', {'user_data': response_string})

# Login page
def login(request):
    return render(request, 'byt/login.html')


# Navbar component
def navbar(request):
    return render(request, 'byt/navbar.html')

# Assembly/Filer page aka "Brewery"; assembly means where we "assemble" our wanted device
def brewery(request):
    return render(request, 'byt/brewery.html')
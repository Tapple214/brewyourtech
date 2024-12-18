from django.shortcuts import render

from .models import *

# Create your views here.

# Index/Home page
def index(request):
    response_string = User.objects.all()[0]
    return render(request, 'byt/index.html', {'user_data': response_string})

# Login page
def login(request):
    return render(request, 'byt/login.html')


# Login page
def navbar(request):
    return render(request, 'byt/navbar.html')
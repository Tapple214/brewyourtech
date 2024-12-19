from django.shortcuts import render

from .models import *
from .forms import CSVUploadForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# Views

# Index/Home page aka "Brew Log"
def brewLog(request):
    response_string = User.objects.all()[0]
    return render(request, 'byt/brewLog.html', {'user_data': response_string})

# Login page
def loginSignUp(request):
    if request.method == "POST":
        action = request.POST.get("action")
        name = request.POST.get("name")
        password = request.POST.get("password")

        if action == "signup":
            # Check if the user already exists
            if User.objects.filter(name=name).exists():
                messages.error(request, "Oops! This username already exists! Please login instead.")
            else:
                # Create a new user
                hashed_password = make_password(password)
                User.objects.create(name=name, password=hashed_password)
                messages.success(request, "Yay! Sign-up successful! Please re-enter your input and hit login!")
            return redirect("loginSignUp")  

        elif action == "login":
            # Authenticate the user
            try:
                user = User.objects.get(name=name)
                if check_password(password, user.password):
                    messages.success(request, f"Welcome back, {name}!")
                    # Implement session or redirect logic here
                    return redirect("home")  # Replace with your homepage URL or view
                else:
                    messages.error(request, "Uh oh.. The password you entered is invalid. Please try again!")
            except User.DoesNotExist:
                messages.error(request, "Oops! It seems this user doesn’t exist yet. If you’re new here, please sign up to get started!")
            return redirect("loginSignUp")  

    return render(request, "byt/loginSignUp.html") 

# Assembly/Filter page aka "Brewery"; Assembly indicated page/location where we "assemble" our wanted device
def brewery(request):
    # Query all phone data
    phone_data = Phone.objects.all()
    
    # Categories for dynamic cards
    categories = [
        {
            "id": "phone",
            "name": "Phones",
            "icon": "bi-phone",
            "svg_path": "<path d='M11 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM5 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z' /><path d='M8 14a1 1 0 1 0 0-2 1 1 0 0 0 0 2' />",
            "form_template": "byt/phoneForm.html",
        },
        {
            "id": "laptop",
            "name": "Laptops",
            "icon": "bi-laptop",
            "svg_path": "<path d='M13.5 3a.5.5 0 0 1 .5.5V11H2V3.5a.5.5 0 0 1 .5-.5zm-11-1A1.5 1.5 0 0 0 1 3.5V12h14V3.5A1.5 1.5 0 0 0 13.5 2zM0 12.5h16a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 12.5' />",
            "form_template": "byt/laptopForm.html",
        },
        {
            "id": "camera",
            "name": "Cameras",
            "icon": "bi-camera",
            "svg_path": "<path d='M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 1 3.172 4z' /><path d='M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0' />",
            "form_template": "byt/cameraForm.html",
        }, 
        {
            "id": "tablet",
            "name": "Tablets",
            "icon": "bi-tablet",
            "svg_path": "<path d='M12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z' /><path d='M8 14a1 1 0 1 0 0-2 1 1 0 0 0 0 2' />",
            "form_template": "byt/tabletForm.html",
        },
    ]

    # Merge the context for rendering
    context = {
        "categories": categories,
        "phone_data": phone_data,
    }

    return render(request, "byt/brewery.html", context)


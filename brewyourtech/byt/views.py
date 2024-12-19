### START ###

from .models import *
from .forms import CSVUploadForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User

# Views

# Login page
def loginSignUp(request):
    if request.method == "POST":
        action = request.POST.get("action")
        name = request.POST.get("name")
        password = request.POST.get("password")

        if action == "signup":
            if User.objects.filter(name=name).exists():
                # If user exists
                messages.error(request, "Oops! This username already exists! Please login instead.")
            else:
                # If user DOES NOT exist create a new user
                hashed_password = make_password(password)
                User.objects.create(name=name, password=hashed_password)
                messages.success(request, "Yay! Sign-up successful! Please re-enter your input and hit login!")
            return redirect("loginSignUp")  

        elif action == "login":
            try:
                user = User.objects.get(name=name)
                if check_password(password, user.password):
                    # If user exists
                    messages.success(request, f"Welcome back, {name}!")
                    # TODO: Implement session or redirect logic here
                    return redirect('brewLog')  
                else:
                    # If user DOES NOT exist
                    messages.error(request, "Uh oh.. The password you entered is invalid. Please try again!")
            except User.DoesNotExist:
                messages.error(request, "Oops! It seems this user doesn’t exist yet. If you’re new here, please sign up to get started!")
            return redirect("loginSignUp")  

    return render(request, "byt/loginSignUp.html") 

# Index/Home page aka "Brew Log"
def brewLog(request):
    response_string = User.objects.all()[0]
    return render(request, 'byt/brewLog.html', {'user_data': response_string})

# Phone Filter page
def phoneBrew(request):
    if request.method == "GET":
        # Take in form inputs/GET params
        price = request.GET.get("price", None)
        launch_year = request.GET.get("launch_year", None)
        ram = request.GET.get("ram", None)
        main_camera = request.GET.get("main_camera", None)
        selfie_camera = request.GET.get("selfie_camera", None)
        sound_jack = request.GET.get("sound_jack", None)
        bluetooth = request.GET.get("bluetooth", None)
        battery_capacity = request.GET.get("battery_capacity", None)

        # Initialize filters dictionary
        filters = {}

        # lte = less than equal to
        # gte = greater than equal to
        # Add inputs to filter
        if price:
            filters["price_usd__lte"] = price 
        if launch_year:
            filters["launch_expected_year__gte"] = launch_year  
        if ram:
            filters["ram_gb__gte"] = float(ram) / 1024  # Convert MB to GB
        if main_camera:
            filters["main_camera_single_mp__gte"] = main_camera
        if selfie_camera:
            filters["selfie_camera_single_mp__gte"] = selfie_camera
        if sound_jack:
            filters["sound_3_5mm_jack"] = sound_jack == "Yes"
        if bluetooth:
            filters["comms_bluetooth__gte"] = bluetooth
        if battery_capacity:
            filters["battery_capacity_mah__gte"] = battery_capacity

        # Query the Phone model with the filters
        phones = Phone.objects.filter(**filters)

        # Pass the filtered phones to the template context
        return render(request, "byt/phoneBrew.html", {"phones": phones})

# TODO: clean
def laptopBrew(request):
    if request.method == "GET":
        # Take in form inputs/GET params
        price = request.GET.get("price", None)
        ram = request.GET.get("ram", None)  # Updated to match 'ram' field in model
        inches = request.GET.get("inches", None)  # Updated to match 'inches' field in model
        cpu_company = request.GET.get("cpu_company", None)  # Updated to match 'cpu_company' field in model

        # Initialize filters dictionary
        filters = {}

        # Add inputs to filters
        if price:
            filters["price_euros__gte"] = price  
        if ram:
            filters["ram__gte"] = ram  # Greater than or equal to RAM
        if inches:
            filters["inches__gte"] = inches  # Minimum screen size in inches
        # Only apply the CPU company filter if a specific value is selected (not "All" or empty)
        if cpu_company and cpu_company.strip():  # Ensure 'All' (empty) option doesn't filter
            filters["cpu_company__icontains"] = cpu_company  # Case-insensitive match for CPU company

        # Query the Laptop model with the filters
        laptops = Laptop.objects.filter(**filters)

        # Pass the filtered laptops to the template context
        return render(request, "byt/laptopBrew.html", {"laptops": laptops})
    
def cameraBrew(request):
    if request.method == "GET":
        # Take in form inputs/GET params
        price = request.GET.get("price", None)
        max_resolution = request.GET.get("max_resolution", None)
        zoom_tele = request.GET.get("zoom_tele", None)

        # Initialize filters dictionary
        filters = {}

        # Add inputs to filters
        if price:
            filters["price__lte"] = price  # Less than or equal to price
        if max_resolution:
            filters["max_resolution__gte"] = max_resolution  # Greater than or equal to max resolution
        if zoom_tele:
            filters["zoom_tele__gte"] = zoom_tele  # Greater than or equal to zoom tele

        # Query the Camera model with the filters
        cameras = Camera.objects.filter(**filters)

        # Pass the filtered cameras to the template context
        return render(request, "byt/cameraBrew.html", {"cameras": cameras})

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
            "link": "/phoneBrew",
        },
        {
            "id": "laptop",
            "name": "Laptops",
            "icon": "bi-laptop",
            "svg_path": "<path d='M13.5 3a.5.5 0 0 1 .5.5V11H2V3.5a.5.5 0 0 1 .5-.5zm-11-1A1.5 1.5 0 0 0 1 3.5V12h14V3.5A1.5 1.5 0 0 0 13.5 2zM0 12.5h16a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 12.5' />",
            "link": "/laptopBrew",
        },
        {
            "id": "camera",
            "name": "Cameras",
            "icon": "bi-camera",
            "svg_path": "<path d='M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 1 3.172 4z' /><path d='M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0' />",
            "link": "/cameraBrew",
        }, 
        {
            "id": "tablet",
            "name": "Tablets",
            "icon": "bi-tablet",
            "svg_path": "<path d='M12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z' /><path d='M8 14a1 1 0 1 0 0-2 1 1 0 0 0 0 2' />",
            "link": "byt/tabletForm.html",
        },
    ]

    # Merge the context for rendering
    context = {
        "categories": categories,
        "phone_data": phone_data,
    }

    return render(request, "byt/brewery.html", context)


# TRACKER:
# GET
# POST - login/signup
# PUT
# DELETE
# PATCH??
# TRANSACTIONS

### END ###
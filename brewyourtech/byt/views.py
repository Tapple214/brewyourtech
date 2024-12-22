### START ###

from .models import *
from .forms import CSVUploadForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    messages.success(request, f"Welcome back, {name}!")
                    return redirect('brewLog')  
                else:
                    # If password is invalid
                    messages.error(request, "Uh oh.. The password you entered is invalid. Please try again!")
            except User.DoesNotExist:
                messages.error(request, "Oops! It seems this user doesn’t exist yet. If you’re new here, please sign up to get started!")
            return redirect("loginSignUp")  

    return render(request, "byt/loginSignUp.html")

# # Fetch the user givent that we are using django hash then we goot do below
# user = User.objects.get(name="Apple")

# # Update the password to a hashed version
# user.password = make_password("123")
# user.save()

def logout(request):
    # Clear the session
    request.session.flush()
    messages.success(request, "You have been logged out successfully!")
    return redirect("loginSignUp")

def brewLog(request):
    # Check if the user is logged in by checking the session
    user_id = request.session.get('user_id')
    
    if not user_id:
        # If no session exists, redirect to the login page
        return redirect('loginSignUp')
    
    try:
        # Fetch the user's profile using the ID stored in the session
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        # Handle the case where the user ID in the session is invalid
        request.session.flush()  # Clear the session
        return redirect('loginSignUp')

    # Fetch all bookmarks for the logged-in user
    bookmarks = Bookmark.objects.filter(user=user)

    # Create a list of bookmarked items
    bookmarked_items = []
    for bookmark in bookmarks:
        item = None
        if bookmark.category == 'phone':
            item = Phone.objects.filter(id=bookmark.item_id).first()
        elif bookmark.category == 'laptop':
            item = Laptop.objects.filter(id=bookmark.item_id).first()
        elif bookmark.category == 'tablet':
            item = Tablet.objects.filter(index=bookmark.item_id).first()
        elif bookmark.category == 'camera':
            item = Camera.objects.filter(id=bookmark.item_id).first()

        if item:
            bookmarked_items.append({
                'category': bookmark.category,
                'item': item,
            })

    # Return a response with the rendered template
    return render(request, 'byt/brewLog.html', {
        'user_data': user,
        'user_id': user_id,
        'bookmarked_items': bookmarked_items,  # Pass resolved items
    })


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
            filters["launch_expected_year__lte"] = launch_year  
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

        user_id = request.session.get('user_id')
        # Pass the filtered phones to the template context
        return render(request, "byt/phoneBrew.html", {"phones": phones, 'user_id': user_id})

# TODO: clean
from currency_converter import CurrencyConverter

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
            filters["price_euros__lte"] = price
        if ram:
            filters["ram__lte"] = ram  # Greater than or equal to RAM
        if inches:
            filters["inches__lte"] = inches  # Minimum screen size in inches
        # Only apply the CPU company filter if a specific value is selected (not "All" or empty)
        if cpu_company and cpu_company.strip():  # Ensure 'All' (empty) option doesn't filter
            filters["cpu_company__icontains"] = cpu_company  # Case-insensitive match for CPU company

        # Query the Laptop model with the filters
        laptops = Laptop.objects.filter(**filters)

        # Initialize CurrencyConverter object for conversion
        c = CurrencyConverter()

        # Convert the price from Euros to USD for each laptop
        laptops_with_converted_prices = []
        for laptop in laptops:
            try:
                laptop.price_usd = round(c.convert(laptop.price_euros, 'EUR', 'USD'), 2)  # Convert and round to 2 decimal places
            except Exception as e:
                laptop.price_usd = "Error"  # Handle conversion error gracefully
            laptops_with_converted_prices.append(laptop)

        user_id = request.session.get('user_id')
        return render(request, "byt/laptopBrew.html", {"laptops": laptops_with_converted_prices, "user_id": user_id})
    
    # TODO: clean find out range of prices, currency and if there is anyway u can convert
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
            filters["max_resolution__lte"] = max_resolution  # Greater than or equal to max resolution
        if zoom_tele:
            filters["zoom_tele__lte"] = zoom_tele  # Greater than or equal to zoom tele

        # Query the Camera model with the filters
        cameras = Camera.objects.filter(**filters)

        user_id = request.session.get('user_id')
        # Pass the filtered cameras to the template context
        return render(request, "byt/cameraBrew.html", {"cameras": cameras, 'user_id': user_id})
    
def tabletBrew(request):
    if request.method == "GET":
        # Take in form inputs/GET params
        price = request.GET.get("price", None)
        display_size_inches = request.GET.get("display_size_inches", None)
        battery_capacity = request.GET.get("battery_capacity", None)

        # Initialize filters dictionary
        filters = {}

        # Add inputs to filters
        if price:
            filters["price__lte"] = price  # Less than or equal to price
        if display_size_inches:
            filters["display_size_inches__lte"] = display_size_inches  # Greater than or equal to display size
        if battery_capacity:
            filters["battery_capacity__lte"] = battery_capacity  # Greater than or equal to battery capacity

        # Query the Tablet model with the filters
        tablets = Tablet.objects.filter(**filters)

        # Initialize CurrencyConverter object for conversion
        c = CurrencyConverter()

        # Convert the price from Indian Rupees to USD for each tablet
        tablets_with_converted_prices = []
        for tablet in tablets:
            try:
                tablet.price_usd = round(c.convert(tablet.price, 'INR', 'USD'), 2)  # Convert and round to 2 decimal places
            except Exception as e:
                tablet.price_usd = "Error"  # Handle conversion error gracefully
            tablets_with_converted_prices.append(tablet)

        user_id = request.session.get('user_id')
        # Pass the filtered tablets to the template context
        return render(request, "byt/tabletBrew.html", {"tablets": tablets_with_converted_prices, 'user_id': user_id})



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
            "description": "Discover a range of smartphones designed to suit your unique needs. Whether you prioritize battery life, camera quality, or affordability, our collection has something for everyone."
        },
        {
            "id": "laptop",
            "name": "Laptops",
            "icon": "bi-laptop",
            "svg_path": "<path d='M13.5 3a.5.5 0 0 1 .5.5V11H2V3.5a.5.5 0 0 1 .5-.5zm-11-1A1.5 1.5 0 0 0 1 3.5V12h14V3.5A1.5 1.5 0 0 0 13.5 2zM0 12.5h16a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 0 12.5' />",
            "link": "/laptopBrew",
            "description": " Explore laptops tailored to a variety of needs, from productivity and gaming to casual use and professional tasks. Whatever your criteria—performance, portability, or price—we have options that fit your lifestyle."
        },
        {
            "id": "camera",
            "name": "Cameras",
            "icon": "bi-camera",
            "svg_path": "<path d='M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828.828A2 2 0 1 3.172 4z' /><path d='M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5m0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7M3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0' />",
            "link": "/cameraBrew",
            "description":"Find the perfect camera for your photography goals. Whether you're a hobbyist capturing memories or a professional seeking precision, our range offers solutions for all skill levels and preferences."
        }, 
        {
            "id": "tablet",
            "name": "Tablets",
            "icon": "bi-tablet",
            "svg_path": "<path d='M12 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1zM4 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2z' /><path d='M8 14a1 1 0 1 0 0-2 1 1 0 0 0 0 2' />",
            "link": "/tabletBrew",
            "description":"Browse tablets that cater to diverse requirements, from entertainment and learning to work and creative projects. With options that balance portability, power, and versatility, there's something for every need."
        },
    ]

    # Merge the context for rendering
    context = {
        "categories": categories,
        "phone_data": phone_data,
    }

    return render(request, "byt/brewery.html", context)

def brewDisplay(request, device_type, device_id, user_id):
    # Fetch the device based on the device_type
    device = None
    if device_type == "tablet":
        device = get_object_or_404(Tablet, index=device_id)
    elif device_type == "phone":
        device = get_object_or_404(Phone, id=device_id)
    elif device_type == "laptop":
        device = get_object_or_404(Laptop, id=device_id)
    elif device_type == "camera":
        device = get_object_or_404(Camera, id=device_id)
    else:
        return render(request, "404.html", {"message": "Invalid device type"})

    # Fetch the user
    user = get_object_or_404(User, id=user_id)

    # Check if the device is bookmarked
    is_bookmarked = Bookmark.objects.filter(
        user=user,
        category=device_type,
        item_id=device_id
    ).exists()

    # Pass the data to the template
    return render(request, 'byt/brewDisplay.html', {
        "device": device,
        "device_type": device_type,
        "is_bookmarked": is_bookmarked,
        "user_id": user_id,
    })

@csrf_exempt # Temporarily exempt from CSRF for testing; remove this for production
# @login_required  # Ensure only logged-in users can access this view
def toggle_bookmark(request):
    # Check if user is logged in via session
    user_id = request.session.get('user_id')
    
    if not user_id:
        return JsonResponse({"success": False, "message": "You must be logged in to bookmark items"}, status=401)

    # Validate the user exists
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"success": False, "message": "User does not exist"}, status=404)

    if request.method == "POST":
        # Parse JSON payload
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON"}, status=400)

        # Extract data
        category = data.get("category")
        item_id = data.get("item_id")

        # Validate input
        if not category or not item_id:
            print(f"Debug: category = {category}, item_id = {item_id}")
            return JsonResponse({"success": False, "message": "Invalid data"}, status=400)


        # Check if the bookmark already exists
        bookmark = Bookmark.objects.filter(user=user, category=category, item_id=item_id).first()
        if bookmark:
            # Remove bookmark if it exists
            bookmark.delete()
            return JsonResponse({"success": True, "message": "Bookmark removed"})
        else:
            # Create a new bookmark if it doesn't exist
            Bookmark.objects.create(user=user, category=category, item_id=item_id)
            return JsonResponse({"success": True, "message": "Bookmark added"})

    # Return method not allowed for non-POST requests
    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)


# TRACKER:
# GET
# POST - login/signup
# PUT
# DELETE
# PATCH??
# TRANSACTIONS

### END ###
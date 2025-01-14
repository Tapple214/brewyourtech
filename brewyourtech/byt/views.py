### START ###

from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from currency_converter import CurrencyConverter


# Views
# HyperLink Views
def mainPage(request):
    return render(request, 'byt/main.html')

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
                    print(password, user.password)
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


def logout(request):
    # Clear the session
    request.session.flush()
    messages.success(request, "You have been logged out successfully!")
    return redirect("loginSignUp")

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
    # Initialize the device and the price conversion object
    device = None
    c = CurrencyConverter()  # Currency converter instance

    # Handle device type logic
    if device_type == "tablet":
        device = get_object_or_404(Tablet, index=device_id)
        # Convert price from INR to USD for tablets
        try:
            device.price_usd = round(c.convert(device.price, 'INR', 'USD'), 2)
        except Exception as e:
            device.price_usd = "Error"  # Handle any error gracefully

    elif device_type == "phone":
        device = get_object_or_404(Phone, id=device_id)
        # Convert price from local currency (USD assumed) to USD for phones (no conversion needed)
        device.price_usd = device.price_usd  

    elif device_type == "laptop":
        device = get_object_or_404(Laptop, id=device_id)
        # Convert price from EUR to USD for laptops
        try:
            device.price_usd = round(c.convert(device.price_euros, 'EUR', 'USD'), 2)
        except Exception as e:
            device.price_usd = "Error"  # Handle any error gracefully

    elif device_type == "camera":
        device = get_object_or_404(Camera, id=device_id)
        # Convert price from local currency (USD assumed) to USD for cameras (no conversion needed)
        device.price_usd = device.price  # Assuming price is already in USD or needs no conversion

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

### END ### 
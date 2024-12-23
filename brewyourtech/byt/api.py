### START ###

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Bookmark, Phone, Laptop, Tablet, Camera, User
from currency_converter import CurrencyConverter
from .forms import PhoneFilterForm, CameraFilterForm, LaptopFilterForm, TabletFilterForm
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from .serializers import PhoneSerializer, LaptopSerializer, TabletSerializer, CameraSerializer, BookmarkSerializer

class BrewLogView(View):
    def get(self, request):
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
        c = CurrencyConverter()  # Initialize CurrencyConverter object

        for bookmark in bookmarks:
            item = None
            if bookmark.category == 'phone':
                item = Phone.objects.filter(id=bookmark.item_id).first()
            elif bookmark.category == 'laptop':
                item = Laptop.objects.filter(id=bookmark.item_id).first()
                # Convert the price from Euros to USD for laptops
                if item:
                    try:
                        item.price_usd = round(c.convert(item.price_euros, 'EUR', 'USD'), 2)
                    except Exception as e:
                        item.price_usd = "Error"  # Handle conversion error gracefully
            elif bookmark.category == 'tablet':
                item = Tablet.objects.filter(index=bookmark.item_id).first()
                # Convert the price from INR to USD for tablets
                if item:
                    try:
                        item.price_usd = round(c.convert(item.price, 'INR', 'USD'), 2)
                    except Exception as e:
                        item.price_usd = "Error"  # Handle conversion error gracefully
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
            'bookmarked_items': bookmarked_items,  # Pass resolved items directly without serialization
        })

class PhoneBrewView(View):
    def get(self, request):
        form = PhoneFilterForm(request.GET)

        if form.is_valid():  # If the form data is valid
            filters = {}

            if form.cleaned_data["price"]:
                filters["price_usd__lte"] = form.cleaned_data["price"]
            if form.cleaned_data["launch_year"]:
                filters["launch_expected_year__lte"] = form.cleaned_data["launch_year"]
            if form.cleaned_data["ram"]:
                filters["ram_gb__lte"] = form.cleaned_data["ram"] / 1024  # Convert MB to GB
            if form.cleaned_data["main_camera"]:
                filters["main_camera_single_mp__lte"] = form.cleaned_data["main_camera"]
            if form.cleaned_data["selfie_camera"]:
                filters["selfie_camera_single_mp__lte"] = form.cleaned_data["selfie_camera"]
            if form.cleaned_data["sound_jack"]:
                filters["sound_3_5mm_jack"] = form.cleaned_data["sound_jack"] == "Yes"
            if form.cleaned_data["bluetooth"]:
                filters["comms_bluetooth__lte"] = form.cleaned_data["bluetooth"]
            if form.cleaned_data["battery_capacity"]:
                filters["battery_capacity_mah__lte"] = form.cleaned_data["battery_capacity"]

            phones = Phone.objects.filter(**filters)
        else:
            phones = Phone.objects.all()

        # Serialize the phones data
        serialized_phones = PhoneSerializer(phones, many=True)

        user_id = request.session.get('user_id')
        return render(request, "byt/phoneBrew.html", {"phones": serialized_phones.data, 'user_id': user_id, 'form': form})

class CameraBrewView(View):
    def get(self, request):
        form = CameraFilterForm(request.GET)

        if form.is_valid():  # If the form data is valid
            filters = {}

            # Price Filter
            if form.cleaned_data["price"]:
                filters["price__lte"] = form.cleaned_data["price"]  # Less than or equal to price

            # Max Resolution Filter
            if form.cleaned_data["max_resolution"]:
                filters["max_resolution__lte"] = form.cleaned_data["max_resolution"]  

            # Release Date Filter
            if form.cleaned_data["release_date"]:
                filters["release_date__lte"] = form.cleaned_data["release_date"]  

            # Apply filters to the Camera queryset
            cameras = Camera.objects.filter(**filters)
        else:
            cameras = Camera.objects.all()  # Return all cameras if form is invalid or empty

        # Serialize the cameras data
        serialized_cameras = CameraSerializer(cameras, many=True)

        user_id = request.session.get('user_id')
        return render(request, "byt/cameraBrew.html", {"cameras": serialized_cameras.data, 'user_id': user_id, 'form': form})

class LaptopBrewView(View):
    def get(self, request):
        form = LaptopFilterForm(request.GET)

        if form.is_valid():
            filters = {}

            if form.cleaned_data["price"]:
                filters["price_euros__lte"] = form.cleaned_data["price"]
            if form.cleaned_data["ram"]:
                filters["ram__lte"] = form.cleaned_data["ram"]
            if form.cleaned_data["inches"]:
                filters["inches__lte"] = form.cleaned_data["inches"]
            if form.cleaned_data["cpu_company"]:
                filters["cpu_company__icontains"] = form.cleaned_data["cpu_company"]

            laptops = Laptop.objects.filter(**filters)
        else:
            laptops = Laptop.objects.all()

        # Initialize CurrencyConverter object for conversion
        c = CurrencyConverter()

        # Convert the price from Euros to USD for each laptop
        laptops_with_converted_prices = []
        for laptop in laptops:
            try:
                laptop.price_usd = round(c.convert(laptop.price_euros, 'EUR', 'USD'), 2)
            except Exception as e:
                laptop.price_usd = "Error"
            laptops_with_converted_prices.append(laptop)

        # Serialize the laptops data
        serialized_laptops = LaptopSerializer(laptops_with_converted_prices, many=True)

        user_id = request.session.get('user_id')
        return render(request, "byt/laptopBrew.html", {"laptops": serialized_laptops.data, "user_id": user_id, "form": form})

class TabletBrewView(View):
    def get(self, request):
        form = TabletFilterForm(request.GET)

        if form.is_valid():
            filters = {}

            if form.cleaned_data["price"]:
                filters["price__lte"] = form.cleaned_data["price"]
            if form.cleaned_data["display_size_inches"]:
                filters["display_size_inches__lte"] = form.cleaned_data["display_size_inches"]
            if form.cleaned_data["battery_capacity"]:
                filters["battery_capacity__lte"] = form.cleaned_data["battery_capacity"]

            tablets = Tablet.objects.filter(**filters)
        else:
            tablets = Tablet.objects.all()

        # Initialize CurrencyConverter object for conversion
        c = CurrencyConverter()

        # Convert the price from INR to USD for each tablet
        tablets_with_converted_prices = []
        for tablet in tablets:
            try:
                tablet.price_usd = round(c.convert(tablet.price, 'INR', 'USD'), 2)
            except Exception as e:
                tablet.price_usd = "Error"
            tablets_with_converted_prices.append(tablet)

        # Serialize the tablets data
        serialized_tablets = TabletSerializer(tablets_with_converted_prices, many=True)

        user_id = request.session.get('user_id')
        return render(request, "byt/tabletBrew.html", {"tablets": serialized_tablets.data, 'user_id': user_id, 'form': form})
    
class ToggleBookmarkView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Ensure the user is being fetched correctly by their id
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)

        category = request.data.get("category")
        item_id = request.data.get("item_id")

        if not category or not item_id:
            return Response({"message": "Invalid data. Both category and item_id are required."}, status=HTTP_400_BAD_REQUEST)

        # Check if the bookmark already exists
        bookmark = Bookmark.objects.filter(user=user, category=category, item_id=item_id).first()

        if bookmark:
            # If the bookmark exists, delete it (toggle off)
            bookmark.delete()
            return Response({"message": "Bookmark removed"}, status=HTTP_200_OK)
        else:
            # Create a new bookmark if it doesn't exist (toggle on)
            bookmark = Bookmark.objects.create(user=user, category=category, item_id=item_id)
            serialized_bookmark = BookmarkSerializer(bookmark)
            return Response({"message": "Bookmark added", "bookmark": serialized_bookmark.data}, status=HTTP_200_OK)

    def delete(self, request):
        # Ensure the user is being fetched correctly by their id
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, id=user_id)

        category = request.data.get("category")
        item_id = request.data.get("item_id")

        if not category or not item_id:
            return Response({"message": "Invalid data. Both category and item_id are required."}, status=HTTP_400_BAD_REQUEST)

        # Check if the bookmark exists
        bookmark = Bookmark.objects.filter(user=user, category=category, item_id=item_id).first()

        if bookmark:
            # Remove the bookmark if it exists
            bookmark.delete()
            return Response({"message": "Bookmark removed"}, status=HTTP_200_OK)
        else:
            return Response({"message": "Bookmark not found."}, status=HTTP_404_NOT_FOUND)
        
### END ###
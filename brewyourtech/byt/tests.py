### START ### 

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from .models import User, Phone, Laptop, Tablet, Camera, Bookmark
from django.test import Client
import json

# To run python manage.py test 
class UserTests(TestCase):

    def setUp(self):
        """Set up a user for login/signup tests."""
        self.client = Client()
        self.user_data = {
            'name': 'testuser',
            'password': 'password123'
        }
        # Create a user
        self.user = User.objects.create(
            name=self.user_data['name'],
            password=make_password(self.user_data['password'])
        )

    # OK 
    def test_user_signup(self):
        """Test the signup functionality."""
        response = self.client.post(reverse('loginSignUp'), {
            'action': 'signup',
            'name': 'newuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        self.assertTrue(User.objects.filter(name='newuser').exists())

    # OK
    def test_user_login(self):
        """Test the login functionality."""
        # Post login data
        response = self.client.post(reverse('loginSignUp'), {
            'action': 'login',
            'name': self.user_data['name'],
            'password': self.user_data['password']
        })
        
        # Check for redirection (302) and that the redirect leads to 'brewLog'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('brewLog'))  # Ensure it's redirecting to brewLog
        
        # Follow the redirect
        response = self.client.get(response.url)
        
        # Check that the user sees the correct welcome message on the brewLog page
        self.assertContains(response, f"Hi {self.user_data['name']}!")  # Adjusted to match actual content

    # OK
    def test_user_logout(self):
        """Test user logout."""
        self.client.login(username=self.user_data['name'], password=self.user_data['password'])
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login page
        self.assertNotIn('_auth_user_id', self.client.session)

class DeviceTests(TestCase):

    # OK
    def setUp(self):
        """Set up some devices for testing."""
        self.client = Client()

        # User setup
        self.user_data = {
            'name': 'testuser',
            'password': 'password123'
        }
        self.user = User.objects.create(
            name=self.user_data['name'],
            password=make_password(self.user_data['password'])
        )
        self.client.login(username=self.user_data['name'], password=self.user_data['password'])

        # Creating test devices with all required fields
        self.phone = Phone.objects.create(
            url="https://example.com",
            brand="Test Phone", 
            model="TP-2023", 
            hits=0, 
            became_fan=10,
            launch_expected_year=2023,
            height_mm=150,
            width_mm=75,
            thickness_mm=8,
            body_weight_g=180,
            display_type="AMOLED",
            pixels_x=1080,
            pixels_y=2400,
            display_size_inches=6.5,
            screen_to_body_ratio=85.0,
            ram_gb=6,
            main_camera_single_mp=48,
            selfie_camera_single_mp=16,
            sound_3_5mm_jack=True,
            comms_bluetooth="5.0",
            comms_nfc=True,
            battery_capacity_mah=4500,
            price_usd=499.99,  
            year_of_warranty=2
        )
        
        self.laptop = Laptop.objects.create(
            company="Test Company",
            product="Test Laptop",
            type_name="Gaming Laptop",
            inches=15.6,
            ram=16,
            operating_system="Windows 10",
            weight=2.5,
            price_euros=800,
            screen_type="IPS",
            screen_width=1920,
            screen_height=1080,
            touchscreen=True,
            ips_panel=True,
            retina_display=False,
            cpu_company="Intel",
            cpu_frequency=2.5,
            cpu_model="i7",
            primary_storage_capacity="1TB",
            secondary_storage_capacity="512GB",
            primary_storage_type="SSD",
            secondary_storage_type="HDD",
            gpu_company="NVIDIA",
            gpu_model="RTX 3060",
            gpu_full_model="RTX 3060 6GB",
            year=2023,
            quarter="Q2",
            architecture="x86",
            process_nm=14,
            cores_shaders="6/1920",
            base_clock_mhz="1200",
            memory_size_gb="16",
            memory_type="DDR4",
            memory_bus_width_bits="128",
            tdp_w="90",
            integrated_gpu=False,
            mobile_gpu=True,
            quantity=100
        )
        
        self.tablet = Tablet.objects.create(
            name="Test Tablet",
            brand="Test Brand",
            rating=4.5,
            price="500",
            processor_brand="Qualcomm",
            num_processor=8,
            processor_speed=2.84,
            ram="4GB",
            memory_inbuilt="128GB",
            battery_capacity="8000mAh",
            charger="Fast Charger",
            charging="USB-C",
            display_size_inches=10.5,
            pixel="IPS",
            resolution_width=1920,
            resolution_height=1200,
            ppi=300,
            frequency_display_hz=60,
            primary_front_camera=8,
            secondary_front_camera=5,
            primary_rear_camera=13,
            secondary_rear_camera=5,
            os_brand="Android",
            version="11",
            memory_card_upto="1TB",
            sim="Nano SIM",
            is_5G=True,
            is_wifi=True
        )
        
        self.camera = Camera.objects.create(
            model="Test Camera",
            release_date=2023,
            max_resolution=64,
            low_resolution=12,
            effective_pixels=50.0,
            zoom_wide=20,
            zoom_tele=4,
            normal_focus_range=30,
            macro_focus_range=10,
            storage_included=128,
            weight=150,
            dimensions="150x80x40 mm",
            price=100
        )

    # OK
    def test_phone_brew_view(self):
            """Test the phoneBrew view with filters."""
            response = self.client.get(reverse('phoneBrew'), {'price_usd': 500})  
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, 'Test Phone')
    # OK
    def test_laptop_brew_view(self):
        """Test the laptopBrew view with filters."""
        response = self.client.get(reverse('laptopBrew'), {'price_euros': 900})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Laptop')

    # OK
    def test_tablet_brew_view(self):
        """Test the tabletBrew view with filters."""
        response = self.client.get(reverse('tabletBrew'), {'price': 500})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Tablet')

    # OK
    def test_camera_brew_view(self):
        """Test the cameraBrew view with filters."""
        response = self.client.get(reverse('cameraBrew'), {'price': 100})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Camera')

class BookmarkTests(TestCase):

    def setUp(self):
        """Set up the user and devices for bookmarking tests."""
        self.client = Client()
        self.user_data = {
            'name': 'testuser',
            'password': 'password123'
        }
        self.user = User.objects.create(
            name=self.user_data['name'],
            password=make_password(self.user_data['password'])
        )
        self.client.login(username=self.user_data['name'], password=self.user_data['password'])

        # Create test devices
        self.phone = Phone.objects.create(
            url="https://example.com",
            brand="Test Phone", 
            model="TP-2023", 
            hits=0, 
            became_fan=10,
            launch_expected_year=2023,
            height_mm=150,
            width_mm=75,
            thickness_mm=8,
            body_weight_g=180,
            display_type="AMOLED",
            pixels_x=1080,
            pixels_y=2400,
            display_size_inches=6.5,
            screen_to_body_ratio=85.0,
            ram_gb=6,
            main_camera_single_mp=48,
            selfie_camera_single_mp=16,
            sound_3_5mm_jack=True,
            comms_bluetooth="5.0",
            comms_nfc=True,
            battery_capacity_mah=4500,
            price_usd=499.99,  
            year_of_warranty=2
        )

    #OK 
    def test_add_bookmark(self):
       # Log in the test user
        self.client.login(username='testuser', password='password123')

        # Manually set the user_id in the session
        session = self.client.session
        session['user_id'] = self.user.id  # Manually setting user_id in session
        session.save()

        # Prepare test data for the bookmark
        data = {
            'category': 'phone',
            'item_id': 1
        }

        # Make a POST request to add the bookmark
        response = self.client.post(reverse('toggle_bookmark'), data, content_type='application/json')

        # Assert that the response status is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check if the bookmark has been added
        bookmark = Bookmark.objects.filter(user=self.user, category='phone', item_id=1).first()
        self.assertIsNotNone(bookmark)

    # OK
    def test_add_bookmark_without_login(self):
        # Prepare test data for the bookmark
        data = {
            'category': 'tech',
            'item_id': 123
        }

        # Make a POST request to add the bookmark without logging in
        response = self.client.post(reverse('toggle_bookmark'), data, content_type='application/json')

        # Assert that the response status is 401 (Unauthorized)
        self.assertEqual(response.status_code, 401)

    #OK 
    def test_remove_bookmark(self):
        """Test removing a bookmark."""
        
        # Create a bookmark for the user
        Bookmark.objects.create(user=self.user, category='phone', item_id=self.phone.id)

        # Log in the user and ensure the session is set
        self.client.login(username='testuser', password='password123')
        
        # Manually set the user_id in the session (if not already set)
        session = self.client.session
        session['user_id'] = self.user.id  # Manually setting user_id in session
        session.save()

        # Make the POST request to remove the bookmark
        response = self.client.post(reverse('toggle_bookmark'), json.dumps({
            'category': 'phone',
            'item_id': self.phone.id
        }), content_type="application/json")

        # Assert that the response status is 200 (success)
        self.assertEqual(response.status_code, 200)
        
        # Assert that the bookmark is removed
        self.assertContains(response, 'Bookmark removed')
        self.assertFalse(Bookmark.objects.filter(user=self.user, category='phone', item_id=self.phone.id).exists())

### END ### 
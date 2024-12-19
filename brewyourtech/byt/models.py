### START ###

from django.db import models

# Step 1: Make the schema changes
# Step 2: RUN python manage.py makemigrations     
# Step 3: RUN  python manage.py migrate 
# (To pre-populate the your db/models)  
# Step 4: RUN the CSV to Fixture codes 

class User(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Phone(models.Model):
    url = models.URLField(max_length=200)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    hits = models.IntegerField()
    became_fan = models.IntegerField()
    launch_expected_year = models.IntegerField()
    height_mm = models.FloatField()
    width_mm = models.FloatField()
    thickness_mm = models.FloatField()
    body_weight_g = models.FloatField()
    display_type = models.CharField(max_length=100)
    pixels_x = models.IntegerField()
    pixels_y = models.IntegerField()
    display_size_inches = models.FloatField()
    screen_to_body_ratio = models.FloatField()
    ram_gb = models.FloatField()
    main_camera_single_mp = models.FloatField(null=True, blank=True) # Allow null values
    selfie_camera_single_mp = models.FloatField(null=True, blank=True)  
    sound_3_5mm_jack = models.BooleanField()
    comms_bluetooth = models.CharField(max_length=100)
    comms_nfc = models.BooleanField()
    battery_capacity_mah = models.IntegerField()
    price_usd = models.FloatField()
    year_of_warranty = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model}"
    # To ensure that display is readable
    # Example Output: Apple iPhone 14




class Tablet(models.Model):
    index = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    rating = models.FloatField()
    price = models.CharField(max_length=100)  
    processor_brand = models.CharField(max_length=100)
    num_processor = models.IntegerField()
    processor_speed = models.FloatField()  
    ram = models.CharField(max_length=100)  
    memory_inbuilt = models.CharField(max_length=100)  
    battery_capacity = models.CharField(max_length=100) 
    charger = models.CharField(max_length=100)
    charging = models.CharField(max_length=100) 
    display_size_inches = models.FloatField() 
    pixel = models.CharField(max_length=100)  
    resolution_width = models.IntegerField()
    resolution_height = models.IntegerField()
    ppi = models.FloatField()  
    frequency_display_hz = models.FloatField(null=True, blank=True)  
    primary_front_camera = models.FloatField(null=True, blank=True)  
    secondary_front_camera = models.FloatField(null=True, blank=True)  
    primary_rear_camera = models.FloatField(null=True, blank=True)  
    secondary_rear_camera = models.FloatField(null=True, blank=True) 
    os_brand = models.CharField(max_length=100) 
    version = models.CharField(max_length=100)  
    memory_card_upto = models.CharField(max_length=100, null=True, blank=True)  
    sim = models.CharField(max_length=100)  
    is_5G = models.BooleanField()
    is_wifi = models.BooleanField()

    def __str__(self):
        return f"{self.name} ({self.brand})"
    # To ensure that display is readable

class Camera(models.Model):
    model = models.CharField(max_length=100)  
    release_date = models.IntegerField()  
    max_resolution = models.IntegerField()  
    low_resolution = models.IntegerField()  
    effective_pixels = models.FloatField() 
    zoom_wide = models.IntegerField()  
    zoom_tele = models.IntegerField() 
    normal_focus_range = models.IntegerField(null=True, blank=True)  
    macro_focus_range = models.IntegerField(null=True, blank=True)  
    storage_included = models.IntegerField()   
    weight = models.IntegerField()   
    dimensions = models.CharField(max_length=100)  
    price = models.FloatField() 

    def __str__(self):
        return f"{self.model} ({self.release_date})"
    # To ensure that display is readable 

# TRACKER (in codes for python manage.py shell):
# from byt.models import Phone
# from byt.models import Laptop
# from byt.models import Tablet
# from byt.models import Camera
# print(Phone.objects.count())
# 3550
# print(Laptop.objects.count())
# 991
# print(Tablet.objects.count())
# 390
# print(Camera.objects.count())
# 1038

# Total entries: 5969 

### END ###
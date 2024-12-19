from django.db import models

# Create your models here.
# Make the scheme change
#  RUN  python manage.py makemigrations     
#  then RUN  python manage.py migrate   
# Then you do the csv to json codes 

class User(models.Model):
    name = models.CharField(max_length=50)

# To import CSV into table 
# Step 1: Create model
# Step 2: Convert CSV to JSON
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
    main_camera_single_mp = models.FloatField(null=True, blank=True)  # Allow null values
    selfie_camera_single_mp = models.FloatField(null=True, blank=True)  # Allow null values
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

class Laptop(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    price = models.FloatField()
    rating = models.FloatField()
    processor_brand = models.CharField(max_length=100)
    processor_tier = models.CharField(max_length=100)
    num_cores = models.IntegerField()
    num_threads = models.IntegerField()
    ram_memory = models.FloatField()  # Assuming RAM is measured in GB
    primary_storage_type = models.CharField(max_length=100)
    primary_storage_capacity = models.IntegerField()  # Assuming capacity is measured in GB
    secondary_storage_type = models.CharField(max_length=100, null=True, blank=True)  # Allow null/blank for optional fields
    secondary_storage_capacity = models.IntegerField(null=True, blank=True)  # Allow null/blank for optional fields
    gpu_brand = models.CharField(max_length=100)
    gpu_type = models.CharField(max_length=100)
    is_touch_screen = models.BooleanField()
    display_size = models.FloatField()  # Assuming size is measured in inches
    resolution_width = models.IntegerField()
    resolution_height = models.IntegerField()
    operating_system = models.CharField(max_length=100)
    year_of_warranty = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.brand} {self.model}"

class Tablet(models.Model):
    index = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    rating = models.FloatField()
    price = models.CharField(max_length=100)  # Changed to CharField to handle strings like '512GB'
    processor_brand = models.CharField(max_length=100)
    num_processor = models.IntegerField()
    processor_speed = models.FloatField()  # Assuming speed is in GHz
    ram = models.CharField(max_length=100)  # Changed to CharField to handle strings like '8GB'
    memory_inbuilt = models.CharField(max_length=100)  # Changed to CharField to handle strings like '128GB'
    battery_capacity = models.CharField(max_length=100)  # Changed to CharField to handle strings like '7000mAh'
    charger = models.CharField(max_length=100)
    charging = models.CharField(max_length=100)  # Describes charging type (e.g., fast charging)
    display_size_inches = models.FloatField()  # Display size in inches
    pixel = models.CharField(max_length=100)  # e.g., "1080 x 2400 pixels"
    resolution_width = models.IntegerField()
    resolution_height = models.IntegerField()
    ppi = models.FloatField()  # Pixels per inch
    frequency_display_hz = models.FloatField(null=True, blank=True)  # Refresh rate in Hz (optional)
    primary_front_camera = models.FloatField(null=True, blank=True)  # Megapixels (optional)
    secondary_front_camera = models.FloatField(null=True, blank=True)  # Megapixels (optional)
    primary_rear_camera = models.FloatField(null=True, blank=True)  # Megapixels (optional)
    secondary_rear_camera = models.FloatField(null=True, blank=True)  # Megapixels (optional)
    os_brand = models.CharField(max_length=100)  # e.g., "Android", "iOS"
    version = models.CharField(max_length=100)  # OS version
    memory_card_upto = models.CharField(max_length=100, null=True, blank=True)  # Changed to CharField to handle strings like '2TB'
    sim = models.CharField(max_length=100)  # SIM type (e.g., "Single SIM", "Dual SIM")
    is_5G = models.BooleanField()
    is_wifi = models.BooleanField()

    def __str__(self):
        return f"{self.name} ({self.brand})"

class Camera(models.Model):
    model = models.CharField(max_length=100)  # Camera model name
    release_date = models.IntegerField()  # Release year
    max_resolution = models.IntegerField()  # Maximum resolution (e.g., 1024)
    low_resolution = models.IntegerField()  # Low resolution (e.g., 640)
    effective_pixels = models.FloatField()  # Effective pixels (in MP, allows decimals)
    zoom_wide = models.IntegerField()  # Zoom wide (W) in mm
    zoom_tele = models.IntegerField()  # Zoom tele (T) in mm
    normal_focus_range = models.IntegerField(null=True, blank=True)  # Normal focus range in cm (optional)
    macro_focus_range = models.IntegerField(null=True, blank=True)  # Macro focus range in cm (optional)
    storage_included = models.IntegerField()  # Storage included in MB
    weight = models.IntegerField()  # Weight (including batteries) in grams
    dimensions = models.CharField(max_length=100)  # Dimensions (e.g., "95 x 158")
    price = models.FloatField()  # Price in USD

    def __str__(self):
        return f"{self.model} ({self.release_date})"
    

    # from byt.models import Phone
#  from byt.models import Laptop
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

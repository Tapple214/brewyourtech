from django.db import models

# Create your models here.

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

    def __str__(self):
        return f"{self.brand} {self.model}"

    
    # To ensure that display is readable
    # Example Output: Apple iPhone 14
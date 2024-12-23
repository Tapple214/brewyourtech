### START ###

from django.contrib import admin
from .models import User, Phone, Laptop, Camera, Tablet, Bookmark

admin.site.register(User)
admin.site.register(Phone)
admin.site.register(Laptop)
admin.site.register(Camera)
admin.site.register(Tablet)
admin.site.register(Bookmark)

### END ###
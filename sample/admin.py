from django.contrib import admin
from .models import Booking




admin.site.register(Booking)
from .models import Contact  # Ensure this import statement is correct

admin.site.register(Contact)
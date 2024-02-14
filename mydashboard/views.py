from django.shortcuts import render

# Create your views here.
# mydashboard/views.py

from django.shortcuts import render
from sample.models import Booking

def index(request):
    # Retrieve booking data from the database
    bookings = Booking.objects.all()  # Assuming you want to retrieve all bookings

    # Pass the booking data to the template context
    context = {
        'bookings': bookings  # This will make the 'bookings' queryset available in your template
    }

    # Render the template with the provided context
    return render(request, 'mydashboard/index.html', context)


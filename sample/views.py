from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect
from sample.models import Booking
from django.utils.dateparse import parse_date






def index(request):
    # Get total room counts for each room type
    total_standard_rooms = 12  # Replace with your actual total standard rooms count
    total_deluxe_rooms = 12  # Replace with your actual total deluxe rooms count
    total_suite_rooms = 2  # Replace with your actual total suite rooms count

    # Get current date
    current_date = datetime.now().date()

    # Query bookings that have checkout date equal to the current date
    ended_bookings = Booking.objects.filter(checkout_date=current_date)

    # Initialize counts for each room type
    standard_count = 0
    deluxe_count = 0
    suite_count = 0

    # Iterate over ended bookings to count booked rooms of each type
    for booking in ended_bookings:
        if booking.room_type == 'Standard':
            standard_count += 1
        elif booking.room_type == 'Deluxe':
            deluxe_count += 1
        elif booking.room_type == 'Suite':
            suite_count += 1

    # Calculate available rooms by subtracting booked rooms from total rooms
    available_standard_rooms = total_standard_rooms - standard_count
    available_deluxe_rooms = total_deluxe_rooms - deluxe_count
    available_suite_rooms = total_suite_rooms - suite_count

    context = {
        'total_standard_rooms': total_standard_rooms,
        'total_deluxe_rooms': total_deluxe_rooms,
        'total_suite_rooms': total_suite_rooms,
        'standard_count': standard_count,
        'deluxe_count': deluxe_count,
        'suite_count': suite_count,
        'available_standard_rooms': available_standard_rooms,
        'available_deluxe_rooms': available_deluxe_rooms,
        'available_suite_rooms': available_suite_rooms,
    }


    return render(request, 'index.html',context)
def about(request):

    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
from django.utils.dateparse import parse_date
from django.shortcuts import redirect, render
from django.urls import reverse
from .models import Booking
from django.utils.dateparse import parse_date
from urllib.parse import urlencode


def booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        checkin_date_str = request.POST.get('checkin')
        checkout_date_str = request.POST.get('checkout')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        room_type = request.POST.get('room_type')
        amount = request.POST.get('amount')
        room_number = request.POST.get('room_number')
        address = request.POST.get("address")
        number = request.POST.get('number')

        # Parse the date strings to Python date objects
        checkin_date = parse_date(checkin_date_str)
        checkout_date = parse_date(checkout_date_str)

        # Create and save the booking
        booking = Booking.objects.create(
            name=name,
            email=email,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            adults=adults,
            children=children,
            room_type=room_type,
            amount=amount,
            room_number=room_number,
            address=address,
            number=number,
        )
        print(booking)
        # Generate the receipt and get its path
        receipt_path = generate_receipt(booking)

        # Redirect to download_receipt with the receipt path
        # Ensure the path is URL-encoded to handle special characters
        query_string = urlencode({'path': receipt_path})
        download_url = reverse('download_receipt') + '?' + query_string
        print("Redirecting to:", download_url)


    # If not a POST request or after saving a new booking, just render the booking form
    return render(request, 'booking.html')


from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
import os
from urllib.parse import quote
from datetime import datetime

def generate_receipt(booking):
    current_date = datetime.now().strftime('%Y-%m-%d')
    checkin_date = booking.checkin_date.strftime('%Y-%m-%d') if booking.checkin_date else 'N/A'
    checkout_date = booking.checkout_date.strftime('%Y-%m-%d') if booking.checkout_date else 'N/A'

    # Initialize a new blank image with specified background color
    img = Image.new('RGB', (344, 500), color=(255, 255, 255))  # white background
    d = ImageDraw.Draw(img)

    # Define fonts
    title_font_path = os.path.join(settings.BASE_DIR, "static", "deps", "receipt", "DejaVuSans-Bold.ttf")
    title_font = ImageFont.truetype(title_font_path, 24)  # Larger font for title
    content_font = ImageFont.truetype(title_font_path, 16)
    highlight_font = ImageFont.truetype(title_font_path, 18)  # Slightly larger for important details

    # Define colors
    header_color = (3, 101, 100)  # Dark teal
    text_color = (36, 36, 36)  # Almost black
    highlight_color = (255, 127, 80)  # Coral

    # Optionally, load a hotel logo
    logo_path = os.path.join(settings.BASE_DIR, "static", "deps", "receipt", "hotel_logo.png")
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        img.paste(logo, (122, 20), logo)  # Center the logo

    y_offset = logo.height + 30 if os.path.exists(logo_path) else 20  # Adjust start y position based on logo presence

    # Header
    d.text((20, y_offset), "Lotels Receipt", fill=header_color, font=title_font)
    y_offset += 60  # Space after the header

    # Booking details with highlights
    details = [
        ("Name:", booking.name),
        ("Email:", booking.email),
        ("Check-In Date:", checkin_date, highlight_color),
        ("Check-Out Date:", checkout_date, highlight_color),
        ("Adults:", str(booking.adults)),
        ("Children:", str(booking.children)),
        ("Room Type:", booking.room_type),
        ("Amount:", f"${booking.amount}", highlight_color),
        ("Room Number:", booking.room_number),
        ("Address:", booking.address),
        ("Contact Number:", booking.number),
        ("Date Issued:", current_date),
    ]

    for detail in details:
        text, value = detail[:2]
        color = detail[2] if len(detail) == 3 else text_color
        font = highlight_font if len(detail) == 3 else content_font
        d.text((20, y_offset), f"{text} {value}", fill=color, font=font)
        y_offset += 30  # Increment for next entry

    # Save the receipt
    receipts_dir = os.path.join(settings.MEDIA_ROOT, 'receipts', current_date)
    os.makedirs(receipts_dir, exist_ok=True)

    receipt_filename = f"receipt_{booking.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
    receipt_path = os.path.join(receipts_dir, receipt_filename)
    img.save(receipt_path)

    return receipt_path

def generate_receipt_view(request):
    if request.method == "POST":
        try:
            # Assume Booking model exists with appropriate fields
            booking = Booking(
                name=request.POST.get("name"),
                email=request.POST.get("email"),
                checkin_date=request.POST.get("checkin"),
                checkout_date=request.POST.get("checkout"),
                adults=request.POST.get("adults"),
                children=request.POST.get("children"),
                room_type=request.POST.get("room_type"),
                amount=request.POST.get("amount"),
                room_number=request.POST.get("room_number"),
                address=request.POST.get("address"),
                number=request.POST.get("number"),
            )
            # Save the booking
            booking.save()

            # Generate receipt
            receipt_path = generate_receipt(booking)

            # URL-encode the receipt path if it contains special characters
            encoded_receipt_path = quote(receipt_path)

            # Redirect to the receipt page
            return redirect(f'/show-receipt/?path={encoded_receipt_path}')
        except Exception as e:
            return HttpResponse(f"Error: {e}")

def show_receipt(request):
    receipt_path = request.GET.get("path")
    return render(request, 'receipt.html', {'receipt_path': receipt_path})

def download_receipt(request):
    receipt_path = request.GET.get("path")
    file_path = os.path.join(settings.MEDIA_ROOT, receipt_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="image/jpeg")
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
    else:
        raise Http404("The requested receipt does not exist.")

from django.http import JsonResponse
from datetime import datetime


def check_availability(request):
    if request.method == 'POST':
        checkin_date_str = request.POST.get('checkin')
        checkout_date_str = request.POST.get('checkout')
        room_number = request.POST.get('room_number')

        try:
            # Convert date strings to datetime objects for comparison
            checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d')
            checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d')
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        # Define the room type based on the room number
        if 101 <= int(room_number) <= 110:
            room_type = 'Standard'
        elif 201 <= int(room_number) <= 210:
            room_type = 'Deluxe'
        elif 301 <= int(room_number) <= 302:
            room_type = 'Suite'
        else:
            return JsonResponse({'error': 'Invalid room number'}, status=400)

        # Check if the room is available for the selected dates and room type
        if Booking.objects.filter(room_number=room_number, room_type=room_type, checkin_date__lte=checkout_date, checkout_date__gte=checkin_date).exists():
            available = False
        else:
            available = True

        # Return JSON response indicating availability
        return JsonResponse({'available': available})

    # Handle invalid requests
    return JsonResponse({'error': 'Invalid request'}, status=400)

def rooms(request):
    # Get total room counts for each room type
    total_standard_rooms = 12  # Replace with your actual total standard rooms count
    total_deluxe_rooms = 12  # Replace with your actual total deluxe rooms count
    total_suite_rooms = 2  # Replace with your actual total suite rooms count

    # Get current date
    current_date = datetime.now().date()


    # Query bookings that have checkout date equal to the current date
    ended_bookings = Booking.objects.filter(checkout_date=current_date)

    # Initialize counts for each room type
    standard_count = 0
    deluxe_count = 0
    suite_count = 0

    # Iterate over ended bookings to count booked rooms of each type
    for booking in ended_bookings:
        if booking.room_type == 'Standard':
            standard_count += 1
        elif booking.room_type == 'Deluxe':
            deluxe_count += 1
        elif booking.room_type == 'Suite':
            suite_count += 1

    # Calculate available rooms by subtracting booked rooms from total rooms
    available_standard_rooms = total_standard_rooms - standard_count
    available_deluxe_rooms = total_deluxe_rooms - deluxe_count
    available_suite_rooms = total_suite_rooms - suite_count

    context = {
        'total_standard_rooms': total_standard_rooms,
        'total_deluxe_rooms': total_deluxe_rooms,
        'total_suite_rooms': total_suite_rooms,
        'standard_count': standard_count,
        'deluxe_count': deluxe_count,
        'suite_count': suite_count,
        'available_standard_rooms': available_standard_rooms,
        'available_deluxe_rooms': available_deluxe_rooms,
        'available_suite_rooms': available_suite_rooms,
    }


    return render(request, 'room.html', context)

def services(request):
    return render(request,'service.html')

def header(request):
    return render(request, 'header.html')

# Create your views here.

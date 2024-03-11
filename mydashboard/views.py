from time import timezone

from bottle import redirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from sample.models import Booking
from django.contrib.auth.decorators import login_required
from sample.models import Contact
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('mydashboard_index')
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'mydashboard/login.html')

from django.db.models import Sum
from django.utils import timezone
@csrf_exempt
@login_required(login_url='dashboard_login')
def index(request):
    # Order all bookings from the most recent check-in date to the oldest
    bookings = Booking.objects.all().order_by('-checkin_date')
    today = timezone.now().date()
    today_bookings1 = Booking.objects.filter(checkin_date=today)

    # Calculate the total amount for all bookings
    total_amount = today_bookings1.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Calculate the total amount for bookings paid in cash (case-insensitive)
    total_cash = today_bookings1.filter(payment_method__iexact='cash').aggregate(Sum('total_amount'))['total_amount__sum'] or 0

    # Calculate the total amount for bookings paid via GPay (case-insensitive)
    total_gpay = today_bookings1.filter(payment_method__iexact='Google_pay').aggregate(total=Sum('total_amount'))['total'] or 0

    # Calculate the total amount for bookings paid via Card (case-insensitive)
    total_card = today_bookings1.filter(payment_method__iexact='Card').aggregate(total=Sum('total_amount'))['total'] or 0

    context = {
        'bookings': bookings,
        'total_amount': total_amount,
        'total_cash': total_cash,
        'total_gpay': total_gpay,
        'total_card': total_card,
    }

    return render(request, 'mydashboard/index.html', context)
@csrf_exempt
@login_required(login_url='dashboard_login')
def contact(request):
    contacts = Contact.objects.all()
    context = {
        'contacts': contacts
    }
    return render(request, 'mydashboard/contact.html', context)

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('dashboard_login')




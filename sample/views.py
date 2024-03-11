import json
from django.http import QueryDict
import uuid
from django.views.decorators.csrf import csrf_exempt
from easebuzz_lib.easebuzz_payment_gateway import Easebuzz
from django.utils.dateparse import parse_date
from django.urls import reverse
from .models import Contact
from django.utils.timezone import now
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Booking
from datetime import date
from django.http import JsonResponse
from datetime import datetime

from lotels.settings import (

    MERCHANT_KEY,
    SALT,
    ENV,
)

easebuzzObj = Easebuzz(MERCHANT_KEY, SALT, ENV)



@csrf_exempt
def index(request):
    current_date = now().date()
    total_standard_rooms = 16
    total_deluxe_rooms = 14
    total_suite_rooms = 2

    ongoing_bookings = Booking.objects.filter(checkin_date__lte=current_date, checkout_date__gt=current_date)
    ending_today_bookings = Booking.objects.filter(checkout_date=current_date)

    booked_standard_count = ongoing_bookings.filter(room_type='Standard').count()
    booked_deluxe_count = ongoing_bookings.filter(room_type='Deluxe').count()
    booked_suite_count = ongoing_bookings.filter(room_type='Suite').count()

    available_standard_rooms = total_standard_rooms - booked_standard_count
    available_deluxe_rooms = total_deluxe_rooms - booked_deluxe_count
    available_suite_rooms = total_suite_rooms - booked_suite_count

    checking_out_standard = ending_today_bookings.filter(room_type='Standard').count()
    checking_out_deluxe = ending_today_bookings.filter(room_type='Deluxe').count()
    checking_out_suite = ending_today_bookings.filter(room_type='Suite').count()

    context = {
        'total_standard_rooms': total_standard_rooms,
        'total_deluxe_rooms': total_deluxe_rooms,
        'total_suite_rooms': total_suite_rooms,
        'booked_standard_count': booked_standard_count,
        'booked_deluxe_count': booked_deluxe_count,
        'booked_suite_count': booked_suite_count,
        'available_standard_rooms': available_standard_rooms,
        'available_deluxe_rooms': available_deluxe_rooms,
        'available_suite_rooms': available_suite_rooms,
        'checking_out_standard': checking_out_standard,
        'checking_out_deluxe': checking_out_deluxe,
        'checking_out_suite': checking_out_suite,
    }

    return render(request, 'index.html',context)
@csrf_exempt
def about(request):
    current_date = now().date()
    total_standard_rooms = 16
    total_deluxe_rooms = 14
    total_suite_rooms = 2

    ongoing_bookings = Booking.objects.filter(checkin_date__lte=current_date, checkout_date__gt=current_date)
    ending_today_bookings = Booking.objects.filter(checkout_date=current_date)

    booked_standard_count = ongoing_bookings.filter(room_type='Standard').count()
    booked_deluxe_count = ongoing_bookings.filter(room_type='Deluxe').count()
    booked_suite_count = ongoing_bookings.filter(room_type='Suite').count()

    available_standard_rooms = total_standard_rooms - booked_standard_count
    available_deluxe_rooms = total_deluxe_rooms - booked_deluxe_count
    available_suite_rooms = total_suite_rooms - booked_suite_count

    checking_out_standard = ending_today_bookings.filter(room_type='Standard').count()
    checking_out_deluxe = ending_today_bookings.filter(room_type='Deluxe').count()
    checking_out_suite = ending_today_bookings.filter(room_type='Suite').count()

    context = {
        'total_standard_rooms': total_standard_rooms,
        'total_deluxe_rooms': total_deluxe_rooms,
        'total_suite_rooms': total_suite_rooms,
        'booked_standard_count': booked_standard_count,
        'booked_deluxe_count': booked_deluxe_count,
        'booked_suite_count': booked_suite_count,
        'available_standard_rooms': available_standard_rooms,
        'available_deluxe_rooms': available_deluxe_rooms,
        'available_suite_rooms': available_suite_rooms,
        'checking_out_standard': checking_out_standard,
        'checking_out_deluxe': checking_out_deluxe,
        'checking_out_suite': checking_out_suite,
    }

    return render(request, 'about.html',context)

@csrf_exempt
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        # Create and save the new Contact instance
        contact=Contact.objects.create(name=name, email=email, subject=subject, message=message)
        contact.save()

    return render(request, 'contact.html')




@csrf_exempt
def booking(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        checkin_date_str = request.POST.get('checkin')
        checkout_date_str = request.POST.get('checkout')
        adults = request.POST.get('adults')
        children = request.POST.get('children')
        room_type = request.POST.get('room_type')
        amount   = request.POST.get('amount')
        gst_amount_str = request.POST.get('gst', '0')
        total_amount = request.POST.get('total_amount')
        room_number = request.POST.get('room_number')
        address = request.POST.get("address")
        number = request.POST.get('number')
        select_method = request.POST.get('select_method', '')
        payment_method=request.POST.get("payment_method")

        # Parse the date strings to Python date objects
        checkin_date = parse_date(checkin_date_str)
        checkout_date = parse_date(checkout_date_str)
        try:
            # Convert to float first to handle decimal input, then round to nearest integer
            gst_amount = round(float(gst_amount_str))
        except ValueError:
            return HttpResponse("Invalid GST amount", status=400)

        # Create and save the booking with a unique transaction ID
        txn_id = str(uuid.uuid4())
        booking = Booking.objects.create(
            name=name,
            email=email,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            adults=adults,
            children=children,
            room_type=room_type,
            amount=amount,
            gst_amount=gst_amount,
            total_amount=total_amount,
            room_number=room_number,
            address=address,
            number=number,
            transaction_id=txn_id,
            select_method=select_method,
            payment_method=payment_method,

        )
        booking.save()
        # if select_method == 'direct_walk':
        #     receipt_path = generate_receipt(booking)
        #     booking.receipt_path = receipt_path
        #     booking.save()
        #     messages.success(request, 'Your direct walk-in booking has been successfully saved.')
        #     # Redirect to a confirmation or home page
        #     return redirect('index')
        #     # For non-direct walk-in bookings, initiate online payment
        # else:
        postDict = QueryDict(mutable=True)
        postDict.update({
                "txnid": txn_id,
                "amount": str(round(float(total_amount), 2)),
                "firstname": name,
                "email": email,
                "phone": number,
                "productinfo": room_type,
                "surl": request.build_absolute_uri(reverse("callback")),  # Ensure 'callback' is a valid URL name
                "furl": request.build_absolute_uri(reverse("callback")),
                "udf1": '5',
                "udf2": "",
                "udf3": "",
                "udf4": "",
                "udf5": "",
                "address1": "",
                "address2": "",
                "city": "",
                "state": "",
                "country": "",
                "zipcode": "",
            }
        )

        # Make the QueryDict immutable again
        postDict._mutable = False

        final_response = easebuzzObj.initiatePaymentAPI(postDict)
        result = json.loads(final_response)
        print('result',result)
        # Redirect to the download URL or render a template with the result
        if result["status"] == 1:
            return redirect(result["data"])


    # If the request method is not POST, render the booking form again
    return render(request, 'booking.html')


@csrf_exempt
def payment_success(request, booking_id):
    # Retrieve the booking object from the database or return a 404 error if not found
    booking = get_object_or_404(Booking, id=booking_id)

    # Prepare additional details
    current_date = date.today().strftime("%Y-%m-%d")
    checkin_date = booking.checkin_date.strftime("%Y-%m-%d")
    checkout_date = booking.checkout_date.strftime("%Y-%m-%d")

    # Additional details to be passed to the template
    details = [
        ("Date Issued", current_date),
        ("Name", booking.name),
        ("Email", booking.email),
        ("Check-In Date", checkin_date),
        ("Check-Out Date", checkout_date),
        ("Adults", str(booking.adults)),
        ("Children", str(booking.children)),
        ("Room Type", booking.room_type),
        ("Amount", booking.amount),
        ("12% GST", booking.gst_amount),
        ("Total Amount", f"₹{booking.total_amount}"),
        ("Room Number", f"{booking.room_number}"),
        ("Contact Number", booking.number),
    ]

    # Pass both booking and details to the template context
    context = {
        'booking': booking,
        'details': details,
    }

    # Render the payment_success template with the context
    return render(request, 'payment_success.html', context)


def payment_failure(request):
    return render(request, 'failed.html')


@csrf_exempt
@csrf_exempt
def callback(request):
    try:
        if request.method == "POST":
            TXN_ID = request.POST.get("txnid", "").strip()
            order = Booking.objects.get(transaction_id=TXN_ID)

            if request.POST.get("status") == "success":
                order.status = 'SUCCESS'

                # Update the order status and save it
                order.save()

                # Prepare context with booking details for the template
                context = {
                    'booking': order,  # Pass the booking object to the template
                }

                return render(request, 'payment_success.html', context)
            else:
                # Handle other statuses (e.g., failed payment)
                pass
    except Booking.DoesNotExist:
        # Handle the case where the booking does not exist
        pass
    except Exception as e:
        # Handle other exceptions
        pass

    # Redirect or render a template for failed payments or errors
    return render(request, 'failed.html')



# @csrf_exempt
# def generate_receipt(booking):
#     current_date = datetime.now().strftime('%Y-%m-%d')
#     checkin_date = booking.checkin_date.strftime('%Y-%m-%d') if booking.checkin_date else 'N/A'
#     checkout_date = booking.checkout_date.strftime('%Y-%m-%d') if booking.checkout_date else 'N/A'
#
#     # Load the template image from your static directory
#     template_path = os.path.join(settings.BASE_DIR, "static", "deps", "receipt", "image.jpg")
#     img = Image.open(template_path)
#     d = ImageDraw.Draw(img)
#
#     # Define fonts
#     title_font_path = os.path.join(settings.BASE_DIR, "static", "deps", "receipt", "DejaVuSans-Bold.ttf")
#     title_font = ImageFont.truetype(title_font_path, 104)  # Adjusted for larger title
#     content_font = ImageFont.truetype(title_font_path, 80)
#     highlight_font = ImageFont.truetype(title_font_path, 80)  # Same size for highlighted content
#
#     # Define colors
#     header_color = (255, 127, 80)  # Dark teal for the header
#     text_color = (0, 121, 159)     # Almost black for text
#     highlight_color = (255, 127, 80)  # Coral for highlights
#
#     # Set the start position for the y-axis
#     y_offset = 873  # Adjust based on the layout of your template
#
#     # Header
#     d.text((580, 630), "Lotels Receipt", fill=header_color, font=title_font)
#
#     # Booking details with highlights
#     details = [
#         ("Date Issued", current_date),
#         ("Name", booking.name),
#         ("Email", booking.email),
#         ("Check-In Date", checkin_date,),
#         ("Check-Out Date", checkout_date),
#         ("Adults", str(booking.adults)),
#         ("Children", str(booking.children)),
#         ("Room Type", booking.room_type),
#         ("amount", booking.amount),
#         ("12%_gst", booking.gst_amount),
#         ("total_amount", f"₹{booking.total_amount}"),
#         ("Room Number", f"{booking.room_number}"),
#
#         ("Contact Number", booking.number),
#
#     ]
#
#     # Iterate over the details and draw them on the image
#     for label, value in details:
#         font = highlight_font if "total_amount" in label else content_font
#         d.text((580, y_offset), f"{label}: {value}", fill=header_color if "total_amount" in label else text_color, font=font)
#         y_offset += 140  # Increment y-offset for the next detail
#
#     # Address special handling
#     address_label = "Address:"
#     address_value = booking.address
#     # Wrap the address text to fit the width of your template
#     wrapped_address = textwrap.wrap(address_value, width=40)  # Adjust 'width' as needed
#
#     # Draw the Address label once
#     d.text((592, y_offset), f"{address_label}", fill=text_color, font=content_font)
#     y_offset += 80  # Increment y-offset for the Address label
#
#     # Draw each line of the wrapped address
#     for line in wrapped_address:
#         d.text((592, y_offset), line, fill=text_color, font=content_font)
#         y_offset += 90  # Increment y-offset after each line of the address
#
#     # Save the receipt
#     receipts_dir = os.path.join(settings.MEDIA_ROOT, 'receipts', current_date)
#     os.makedirs(receipts_dir, exist_ok=True)
#     receipt_filename = f"{booking.id}.jpg"
#     receipt_path = os.path.join(receipts_dir, receipt_filename)
#     img.save(receipt_path)
#
#     receipt_relative_path = os.path.join("receipts", current_date, receipt_filename)
#     img.save(os.path.join("media", receipt_relative_path))
#
#     return receipt_relative_path






#
# def download_receipt(request):
#     # Retrieve the receipt file path from the query parameters
#     receipt_filename = request.GET.get('path')
#
#     # Construct the full file path
#     receipt_path = os.path.join(settings.MEDIA_ROOT, receipt_filename)
#
#     # Open the file and prepare the response
#     with open(receipt_path, 'rb') as file:
#         response = HttpResponse(file.read(), content_type='image/jpeg')
#
#     # Set the content-disposition header to trigger a download
#     response['Content-Disposition'] = 'attachment; filename="receipt.jpg"'
#     return response







@csrf_exempt
def check_availability(request):
    if request.method == 'POST':
        checkin_date_str = request.POST.get('checkin')
        checkout_date_str = request.POST.get('checkout')
        room_number = request.POST.get('room_number')

        try:
            checkin_date = datetime.strptime(checkin_date_str, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout_date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        # Assuming room_number ranges are exclusive to each type
        if int(room_number) in range(101, 110) or int(room_number) in range(201, 213) or int(room_number) in range(301, 313):
            bookings = Booking.objects.filter(room_number=room_number, checkin_date__lt=checkout_date, checkout_date__gt=checkin_date)
            available = not bookings.exists()
        else:
            return JsonResponse({'error': 'Invalid room number'}, status=400)

        return JsonResponse({'available': available})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def rooms(request):
    current_date = now().date()
    total_standard_rooms = 16
    total_deluxe_rooms = 14
    total_suite_rooms = 2

    ongoing_bookings = Booking.objects.filter(checkin_date__lte=current_date, checkout_date__gt=current_date)
    ending_today_bookings = Booking.objects.filter(checkout_date=current_date)

    booked_standard_count = ongoing_bookings.filter(room_type='Standard').count()
    booked_deluxe_count = ongoing_bookings.filter(room_type='Deluxe').count()
    booked_suite_count = ongoing_bookings.filter(room_type='Suite').count()

    available_standard_rooms = total_standard_rooms - booked_standard_count
    available_deluxe_rooms = total_deluxe_rooms - booked_deluxe_count
    available_suite_rooms = total_suite_rooms - booked_suite_count

    checking_out_standard = ending_today_bookings.filter(room_type='Standard').count()
    checking_out_deluxe = ending_today_bookings.filter(room_type='Deluxe').count()
    checking_out_suite = ending_today_bookings.filter(room_type='Suite').count()

    context = {
        'total_standard_rooms': total_standard_rooms,
        'total_deluxe_rooms': total_deluxe_rooms,
        'total_suite_rooms': total_suite_rooms,
        'booked_standard_count': booked_standard_count,
        'booked_deluxe_count': booked_deluxe_count,
        'booked_suite_count': booked_suite_count,
        'available_standard_rooms': available_standard_rooms,
        'available_deluxe_rooms': available_deluxe_rooms,
        'available_suite_rooms': available_suite_rooms,
        'checking_out_standard': checking_out_standard,
        'checking_out_deluxe': checking_out_deluxe,
        'checking_out_suite': checking_out_suite,
    }

    return render(request, 'room.html', context)

@csrf_exempt
def services(request):
    return render(request,'service.html')
@csrf_exempt
def header(request):
    return render(request, 'header.html')


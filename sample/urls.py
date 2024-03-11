from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('about/', views.about, name= 'about'),
    path('contact/', views.contact, name= 'contact'),
    path('booking/', views.booking, name= 'booking'),
    path('room/', views.rooms, name= 'room'),
    path('services/', views.services, name= 'services'),
    path('header/',views.header, name= 'header' ),
    path('check_availability/', views.check_availability, name='check_availability'),
    # path('generate-receipt/', views.generate_receipt_view, name='generate_receipt'),
    #path('download-receipt/', views.download_receipt, name='download_receipt'),
    #path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_failure/', views.payment_failure, name='payment_failure'),
    path('callback/', views.callback, name='callback'),
    path('payment-success/<int:booking_id>/',views.payment_success, name='payment_success'),










]
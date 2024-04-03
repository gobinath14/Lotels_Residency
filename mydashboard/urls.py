from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='mydashboard_login'),
    path('index/', views.index, name='mydashboard_index'),
    path('contact/', views.contact, name='mydashboard_contact'),
    path('logout/', views.logout_view, name='logout'),
    path('Add_booking/', views.Add_booking, name='mydashboard_Add_booking'),
    path('check_availability/', views.check_availability, name='check_availability'),
    path('success/', views.success, name='mydashboard_success'),

]








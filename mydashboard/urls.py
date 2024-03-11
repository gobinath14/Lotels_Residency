from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='dashboard_login'),
    path('index/', views.index, name='mydashboard_index'),
    path('contact/', views.contact, name='mydashboard_contact'),
    path('logout/', views.logout_view, name='logout')

]


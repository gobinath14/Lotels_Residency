from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='mydashboard_index'),  # Corrected the import statement and added views.
]


from django.db import models

class Booking(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()
    checkin_date = models.DateField(null=True, blank=True)
    checkout_date = models.DateField(null=True, blank=True)
    adults = models.IntegerField()
    children = models.IntegerField(null=True, blank=True)
    room_type = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField(null=True, blank=True)
    room_number = models.CharField(max_length=10,null=True, blank=True)
    number = models.CharField(max_length=20,null=True, blank=True)


    def __str__(self):
        return f"{self.name}'Booking"


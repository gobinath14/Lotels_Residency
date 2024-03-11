import gst as gst
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
    gst_amount=models.IntegerField(null=True, blank=True)
    total_amount= models.IntegerField(null=True, blank=True)
    room_number = models.CharField(max_length=10,null=True, blank=True)
    number = models.CharField(max_length=20,null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('SUCCESS', 'Success'), ('FAILURE', 'Failure')],default='pending')
    transaction_id = models.CharField(max_length=100,null=True, blank=True)
    SELECT_METHODE_CHOICES = [
        ('no_select', 'No Select'),  # This will be the display string for the default choice
        ('direct_walk', 'Direct Walk'),
        ('website', 'Website'),
    ]
    select_method = models.CharField(max_length=20, choices=SELECT_METHODE_CHOICES, default='no_select',null=True, blank=True)
    PAYMENT_METHOD_CHOICES = [
        ('No Amount', 'No Amount'), # This will be the display string for the default
        ('cash', 'Cash'),
        ('google_pay', 'Google Pay'),
    ]
    payment_method = models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES,default='no amount', blank=True,null=True)




    def __str__(self):
        return f"{self.name}'Booking"
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return self.name
class availability_rooms(models.Model):
    room_101 = models.IntegerField(default=1)
    room_102 = models.IntegerField(default=1)
    room_103 = models.IntegerField(default=1)
    room_104 = models.IntegerField(default=1)
    room_105 = models.IntegerField(default=1)
    room_106 = models.IntegerField(default=1)
    room_107 = models.IntegerField(default=1)
    room_108 = models.IntegerField(default=1)
    room_109 = models.IntegerField(default=1)
    room_201 = models.IntegerField(default=1)
    room_202 = models.IntegerField(default=1)
    room_203 = models.IntegerField(default=1)
    room_204 = models.IntegerField(default=1)
    room_205 = models.IntegerField(default=1)
    room_206 = models.IntegerField(default=1)
    room_207 = models.IntegerField(default=1)
    room_208 = models.IntegerField(default=1)
    room_209 = models.IntegerField(default=1)
    room_301 = models.IntegerField(default=1)
    room_302 = models.IntegerField(default=1)
    room_303 = models.IntegerField(default=1)
    room_304 = models.IntegerField(default=1)
    room_305 = models.IntegerField(default=1)
    room_306 = models.IntegerField(default=1)
    room_307 = models.IntegerField(default=1)
    room_308 = models.IntegerField(default=1)
    room_309 = models.IntegerField(default=1)
    def __str__(self):
        return self.name
# Generated by Django 4.2.7 on 2024-02-06 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0007_delete_room_booking_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='room_number',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
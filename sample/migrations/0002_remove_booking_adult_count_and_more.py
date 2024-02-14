# Generated by Django 4.2.7 on 2024-02-03 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sample', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='adult_count',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='child_count',
        ),
        migrations.AddField(
            model_name='booking',
            name='adults',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='booking',
            name='children',
            field=models.IntegerField(default=0),
        ),
    ]

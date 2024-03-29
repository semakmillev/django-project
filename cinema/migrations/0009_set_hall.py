# Generated by Django 2.2.3 on 2019-07-10 10:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cinema', '0008_booking'),
    ]

    def insertData(apps, schema_editor):
        Hall = apps.get_model('cinema', 'Hall')
        hall = Hall(hall_name='Moscow', hall_length=7, hall_width=20)
        hall.save()
        hall = Hall(hall_name='London', hall_length=4, hall_width=10)
        hall.save()


    operations = [
        migrations.RunPython(insertData),
    ]

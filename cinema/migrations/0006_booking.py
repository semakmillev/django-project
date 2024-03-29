# Generated by Django 2.2.3 on 2019-07-09 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0005_auto_20190709_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('schedule_id', models.IntegerField()),
                ('place_id', models.CharField(max_length=10)),
                ('status', models.CharField(default='CREATED', max_length=10)),
                ('booking_date', models.DateTimeField()),
            ],
            options={
                'index_together': {('schedule_id', 'place_id', 'status')},
            },
        ),
    ]

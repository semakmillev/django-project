# Generated by Django 2.2.3 on 2019-07-09 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0003_auto_20190707_1411'),
    ]

    operations = [
        migrations.RenameField(
            model_name='film_schedule',
            old_name='film_id',
            new_name='film',
        ),
        migrations.RenameField(
            model_name='film_schedule',
            old_name='hall_id',
            new_name='hall',
        ),
    ]
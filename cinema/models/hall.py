from django.db import models


class Hall(models.Model):
    hall_name = models.CharField(max_length=20)
    hall_length = models.IntegerField()
    hall_width = models.IntegerField()

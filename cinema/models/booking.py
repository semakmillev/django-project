from django.db import models


class Booking(models.Model):
    user_id = models.IntegerField()
    schedule_id = models.IntegerField()
    place_id = models.CharField(max_length=10)
    status = models.CharField(max_length=10, default='CREATED')

    class Meta:
        index_together = [
            ("schedule_id", "place_id", "status"),
        ]



    #def save(self):


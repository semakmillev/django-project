from datetime import timedelta
import datetime


from django.db import models

from cinema.exceptions import LogicException
from cinema.models.hall import Hall


class Film(models.Model):
    film_name = models.CharField(max_length=200)
    film_length = models.IntegerField()
    price = models.IntegerField()


class Film_Schedule(models.Model):
    film_id = models.IntegerField()  # models.ForeignKey('film', on_delete=models.CASCADE)
    hall_id = models.IntegerField()  # models.ForeignKey('hall', on_delete=models.CASCADE)
    film_start = models.DateTimeField()

    def save(self, *args, **kwargs):
        film = Film.objects.get(id=self.film_id)
        hall = Hall.objects.get(id=self.hall_id)
        dt_film_start = self.film_start  # datetime.datetime.strptime(self.film_start, '%Y-%m-%dT%H:%M:%SZ')
        dt_film_end = dt_film_start + timedelta(minutes=film.film_length + 25)
        if dt_film_start < dt_film_start.replace(hour=9, minute=0, second=0):
            raise LogicException("Too Early!")
        if dt_film_end >= dt_film_start.replace(hour=23, minute=0, second=0):
            raise LogicException("Too Late!")
        schedule = Film_Schedule.objects \
            .filter(film_start__gte=dt_film_start).filter(film_start__lte=dt_film_end) \
            .exclude(id=self.id).exists()
        if schedule:
            raise LogicException("Hall is busy!")
        # Film_ScheduleSerializer.su
        super(Film_Schedule, self).save(*args, **kwargs)
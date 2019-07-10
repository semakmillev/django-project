from datetime import timedelta
import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models, transaction

# Create your models here.
from django.db import models
from django.utils import timezone

from cinema.models.booking import Booking


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email,and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        try:
            with transaction.atomic():
                user = self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('user_role', "user")
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('user_role', "admin")
        return self._create_user(email, password=password, **extra_fields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    """
    email = models.EmailField(max_length=60, unique=True)
    # first_name = models.CharField(max_length=30, blank=True)
    # last_name = models.CharField(max_length=30, blank=True)
    user_name = models.CharField(max_length=200, blank=True)
    # is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    user_role = models.CharField(max_length=60, default="user")
    # date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


class Film(models.Model):
    film_name = models.CharField(max_length=200)
    film_length = models.IntegerField()
    price = models.IntegerField()


class Hall(models.Model):
    hall_name = models.CharField(max_length=20)
    hall_length = models.IntegerField()
    hall_width = models.IntegerField()


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
            raise Exception("Early!")
        if dt_film_end >= dt_film_start.replace(hour=23, minute=0, second=0):
            raise Exception("Late!")
        schedule = Film_Schedule.objects \
            .filter(film_start__gte=dt_film_start).filter(film_start__lte=dt_film_end) \
            .exclude(id=self.id).exists()
        if schedule:
            raise Exception("Fuck!")
        # Film_ScheduleSerializer.su
        super(Film_Schedule, self).save(*args, **kwargs)



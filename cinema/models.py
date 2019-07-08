from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models, transaction

# Create your models here.
from django.db import models
from django.utils import timezone


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


'''
    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.user_role = instance.user_role('user')
        instance.save()
        return instance
'''


class Film(models.Model):
    film_name = models.CharField(max_length=200)
    film_length = models.IntegerField()
    price = models.IntegerField()


class Hall(models.Model):
    hall_name = models.CharField(max_length=20)
    hall_length = models.IntegerField()
    hall_width = models.IntegerField()


class Film_Schedule(models.Model):
    film_id = models.ForeignKey('Film', on_delete=models.CASCADE)
    hall_id = models.ForeignKey('Hall', on_delete=models.CASCADE)
    film_start = models.DateTimeField()

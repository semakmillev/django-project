from datetime import timedelta
import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin



from cinema.models.booking import Booking
from cinema.models.user import User
from cinema.models.film import Film_Schedule, Film
from cinema.models.hall import Hall



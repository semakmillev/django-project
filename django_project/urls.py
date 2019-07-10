"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from cinema import views
# from cinema.views import add_film, CreateUserAPIView, CreateFilmAPIView, CreateFilmScheduleApiView, \
#    GetFilmScheduleApiView
from cinema.views.booking import create_booking
from cinema.views.film import add_film
from cinema.views import *
from cinema.views.schedule import CreateFilmScheduleApiView, GetFilmScheduleApiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cinema/filmList', views.film.FilmView.as_view(), name="film-list"),
    path('cinema/films/', add_film, name="film-list"),
    path('cinema/films/<int:id>', views.film.FilmView.as_view(), name="film-info"),
    path('cinema/auth', views.authenticate_user),
    path('cinema/check', views.check_authorize),
    path('create', CreateUserAPIView.as_view()),
    path('cinema/film', views.film.CreateFilmAPIView.as_view()),
    path('cinema/schedule', CreateFilmScheduleApiView.as_view()), # да я знаю что можно дописать кастомный аутентификатор
    path('cinema/schedules', GetFilmScheduleApiView.as_view()),
    path('cinema/booking', create_booking),
]

import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import User, Film_Schedule, Film, Hall
from cinema.serializers import FilmScheduleSerializer


class GetFilmScheduleApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        search_date = self.request.query_params.get('search_date', datetime.datetime.now().strftime('%Y-%m-%d'))

        '''[i.film_start,
                Film.objects.get(i.film_id).film_name,
                Film.objects.get(i.film_id).film_price,
                Hall.objects.get(i.hall_id).hall_name]'''
        film_schedules = Film_Schedule.objects.filter(
            film_start__gte=datetime.datetime.strptime(search_date, '%Y-%m-%d'))
        film_schedules_info = {}
        for film_schedule in film_schedules:
            film = Film.objects.get(id=film_schedule.film_id)
            hall = Hall.objects.get(id=film_schedule.hall_id)
            try:
                film_schedules_info[hall.id]['films'].append(
                    {'film_id': film_schedule.film_id,
                     'film_name': film.film_name,
                     'film_price': film.film_price,
                     'film_start': film_schedule.film_start})
            except KeyError as ex:
                film_schedules_info[hall.id] = {}
                film_schedules_info[hall.id]["hall_name"] = hall.hall_name
                film_schedules_info[hall.id]['films'] = []
                film_schedules_info[hall.id]['films'].append(
                    {'film_id': film_schedule.film_id,
                     'film_name': film.film_name,
                     'film_price': film.price,
                     'film_start': film_schedule.film_start}
                )

        return Response({'res': film_schedules_info}, status=status.HTTP_200_OK)


class CreateFilmScheduleApiView(APIView):
    permission_classes = (IsAuthenticated,)

    # @permission_classes((IsAuthenticated,))
    def post(self, request):
        try:
            user = User.objects.get(email=request.user)
            if user.user_role != "admin":
                return Response({'message': 'you are not allowed to do it'}, status=status.HTTP_403_FORBIDDEN)
            # user = User.objects.get(email=email, password=password)
            try:
                film_schedule = Film_Schedule.objects.get(id=request.data['id']) if 'id' in request.data else None
            except ObjectDoesNotExist as ex:
                film_schedule = None

            film_schedule_serializer = FilmScheduleSerializer(data=request.data)
            film_schedule_serializer.is_valid(raise_exception=True)
            '''
            if film_schedule is None:
                film_schedule_serializer.create(request.data)
                film_schedule_serializer.save()
            else:
                film_schedule_serializer.update(film_schedule, request.data)
            '''
            if film_schedule is None:
                film_schedule = film_schedule_serializer.save()
            else:
                film_schedule = film_schedule_serializer.update(film_schedule, request.data)
        except Exception as ex:
            print(ex)
            raise ex
        # print(user.user_name)
        # serializer = UserSerializer(data=user)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response({'res': {'id': film_schedule.id}}, status=status.HTTP_201_CREATED)

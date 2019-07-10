import datetime

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.exceptions import LogicException
from cinema.models import User, Film_Schedule, Film, Hall, Booking
from cinema.serializers import FilmScheduleSerializer


@api_view(['GET'])
@permission_classes([AllowAny, ])
def get_places(request: Request):
    schedule_id = request.query_params.get('schedule')
    schedule = Film_Schedule.objects.get(id=schedule_id)
    hall = Hall.objects.get(id=schedule.hall_id)
    booked_places = Booking.objects.filter(schedule_id=schedule_id)
    list_of_booked_places = {booked_place.place_id: booked_place.status
                             for booked_place in booked_places if booked_place.status in ('PAID', 'CREATED')}
    list_of_places = []
    for row in range(1, hall.hall_length + 1):
        row_places = {}
        row_places['id'] = row
        row_places['places'] = []
        # list_of_booked_places.append()
        for place in range(1, hall.hall_width + 1):
            place_id = 'R%sP%s' % (row, place)
            place_is_busy = 1 if place_id in list_of_booked_places else 0
            row_places['places'].append(place_is_busy)
        list_of_places.append(row_places)
    return Response({'res': list_of_places, 'error': ''}, status=status.HTTP_200_OK)


class GetFilmScheduleApiView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        search_date = self.request.query_params.get('search_date', datetime.datetime.now().strftime('%Y-%m-%d'))

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
                     'film_price': film.price,
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

        return Response({'res': film_schedules_info, 'error': ''}, status=status.HTTP_200_OK)


class CreateFilmScheduleApiView(APIView):
    permission_classes = (IsAuthenticated,)

    # @permission_classes((IsAuthenticated,))
    def post(self, request):
        user = User.objects.get(email=request.user)
        if user.user_role != "admin":
            return Response({'message': 'you are not allowed to do it'}, status=status.HTTP_403_FORBIDDEN)
        # user = User.objects.get(email=email, password=password)
        try:
            film_schedule = Film_Schedule.objects.get(id=request.data['id']) if 'id' in request.data else None
        except ObjectDoesNotExist:
            film_schedule = None

        film_schedule_serializer = FilmScheduleSerializer(data=request.data)
        film_schedule_serializer.is_valid(raise_exception=True)
        try:
            if film_schedule is None:
                film_schedule = film_schedule_serializer.save()
            else:
                film_schedule = film_schedule_serializer.update(film_schedule, request.data)
        except LogicException as ex:
            return ex.get_web_response()
        return Response({'res': {'id': film_schedule.id}, 'error': ''}, status=status.HTTP_201_CREATED)

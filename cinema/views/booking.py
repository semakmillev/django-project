import datetime

from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.exceptions import LogicException
from cinema.models.user import User
from cinema.models.booking import Booking
from cinema.models.film import Film_Schedule
from cinema.serializers.booking import BookingSerializer
import pytz

utc = pytz.UTC


class MakeBookingAPIView(APIView):
    permission_classes = (IsAuthenticated,)


# немного кривоватый, лучше использовать join, но его я заботать, к сожалению, не успел
@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def get_user_bookings(request: Request):
    user_id = request.query_params.get('user_id')
    user: User = User.objects.get(email=request.user)
    user_id = user.id if user_id is None else user_id
    if user.user_role != 'ADMIN' and user.id != user_id:
        return Response({'message': "you don't have permission to watch this information"}, status.HTTP_403_FORBIDDEN)
    bookings = Booking.objects.filter(user_id=user_id)
    booking_info_list = []
    for booking in bookings:
        film_schedule = Film_Schedule.objects.get(id=booking.schedule_id)
        if film_schedule.film_start > datetime.datetime.now().replace(tzinfo=utc) - datetime.timedelta(hours=2):
            booking_info_list.append(
                {'booking_id': booking.id, 'place_id': booking.place_id, 'schedule_id': film_schedule.id, 'status':booking.status})
    return Response({'res': booking_info_list, 'error': ''}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_booking(request: Request):
    user: User = User.objects.get(email=request.user)
    booking_data = {}
    booking_data['user_id'] = user.id
    booking_data['place_id'] = 'R' + str(request.data['row']) + 'P' + str(request.data['place'])
    booking_data['schedule_id'] = request.data['schedule_id']
    booking_serializer = BookingSerializer(data=booking_data)
    booking_serializer.is_valid(raise_exception=True)
    try:
        booking = booking_serializer.save()
    except LogicException as ex:
        return ex.get_web_response()

    return Response({'res': {'booking_id': booking.id}, 'error': ''}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def pay_booking(request: Request):
    try:
        booking = Booking.objects.get(id=request.data['booking_id'])
        schedule = Film_Schedule.objects.get(id=booking.schedule_id)
        print(type(schedule.film_start))
        if schedule.film_start + datetime.timedelta(hours=2) < datetime.datetime.now().replace(tzinfo=utc):
            raise LogicException("It's too late to pay this booking")
        if booking.status == 'PAYED':
            raise LogicException("Booking has already payed")
        booking_serializer = BookingSerializer(data=request.data)
        booking_serializer.pay(booking)
        return Response({'res': 'payed', 'error': ''}, status=status.HTTP_200_OK)
    except LogicException as ex:
        return ex.get_web_response()

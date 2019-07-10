import datetime

from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import User, Booking, Film_Schedule
from cinema.serializers.booking import BookingSerializer
import pytz

utc = pytz.UTC


class MakeBookingAPIView(APIView):
    permission_classes = (IsAuthenticated,)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def create_booking(request: Request):
    user: User = User.objects.get(email=request.user)
    booking_data = {}  # = request.data
    booking_data['user_id'] = user.id
    booking_data['place_id'] = 'R' + str(request.data['row']) + 'P' + str(request.data['place'])
    booking_data['schedule_id'] = request.data['schedule_id']
    booking_serializer = BookingSerializer(data=booking_data)
    booking_serializer.is_valid(raise_exception=True)
    try:
        booking = booking_serializer.save()

    except Exception as ex:
        print(ex)
        raise ex

    return Response({'booking_id': booking.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated, ])
def pay_booking(request: Request):
    '''
    user: User = User.objects.get(email=request.user)
    booking_data = {}  # = request.data
    booking_data['user_id'] = user.id
    booking_data['place_id'] = 'R' + str(request.data['row']) + 'P' + str(request.data['place'])
    booking_data['schedule_id'] = request.data['schedule_id']
    booking_serializer = BookingSerializer(data=booking_data)
    booking_serializer.is_valid(raise_exception=True)
    try:
        booking = booking_serializer.save()

    except Exception as ex:
        print(ex)
        raise ex
    '''
    try:
        booking = Booking.objects.get(id=request.data['booking_id'])
        schedule = Film_Schedule.objects.get(id=booking.schedule_id)
        print(type(schedule.film_start))
        if schedule.film_start + datetime.timedelta(hours=2) < datetime.datetime.now().replace(tzinfo=utc):
            raise Exception('Late!')
        if booking.status == 'PAYED':
            raise Exception('Already Payed')
        booking_serializer = BookingSerializer(data=request.data)
        booking_serializer.pay(booking)
    except Exception as ex:
        print(ex)
        raise ex

    return Response({'res': 'payed'}, status=status.HTTP_201_CREATED)

    '''
    try:
        email = request.data['email']
        password = request.data['password']
        user = None
        try:
            user = User.objects.get(email=email, password=password)
        except ObjectDoesNotExist as ex:
            print("Not exists")
        if user:

            try:
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, SECRET_KEY)
                user_details = {}
                user_details['name'] = user.user_name
                user_details['token'] = token
                user_details['user_id'] = user.id
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)

            except Exception as e:
                raise e
        else:
            print("Here")
            res = {}
            res['error'] = 'can not authenticate with the given credentials or the account has been deactivated'
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'error': 'please provide a email and a password'}
        return Response(res)
    '''

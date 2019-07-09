import jwt
from django.contrib.auth import user_logged_in
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework_jwt.utils import jwt_payload_handler

from cinema.models import Film, User
from cinema.serializers import FilmSerializer, UserSerializer
from django_project.settings import SECRET_KEY


@api_view(["POST", ])
def add_film(request):
    serializer = FilmSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # return Response(data="<rq>" + str(pk) + "</rq>", headers="Content-Type: text/xml")


class FilmView(generics.ListAPIView):
    """
    Returns a list of all authors.
    """
    model = Film
    serializer_class = FilmSerializer
    queryset = Film.objects.all()

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """

        id = self.kwargs['id']
        return Film.objects.filter(id=id)


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
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


@api_view(['POST'])
def check_authorize(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        print(token)
        data = {'token': token}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
        print(user)
        return Response({'res': str(user)}, status=status.HTTP_200_OK)
        # request.user = user
    except ValidationError as v:
        print("validation error", v)
        return Response({'validation_error': str(v)}, status=status.HTTP_200_OK)

    return Response({'res': 'ok'}, status=status.HTTP_200_OK)


class CreateFilmAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # user = request.user
        try:
            user = User.objects.get(email=request.user)
            if user.user_role != "admin":
                return Response({'message': 'you are not allowed to do it'}, status=status.HTTP_403_FORBIDDEN)
            # user = User.objects.get(email=email, password=password)
            print(request.data)
            try:
                film = Film.objects.get(id=request.data['id']) if 'id' in request.data else None
            except ObjectDoesNotExist as ex:
                print(type(ex))
                film = None
            film_serializer = FilmSerializer(data=request.data)
            film_serializer.is_valid(raise_exception=True)
            if film is None:
                film_serializer.create(request.data)
                film_serializer.save()
            else:
                film_serializer.update(film, request.data)
        except Exception as ex:
            print(ex)
            raise ex

        # print(user.user_name)
        # serializer = UserSerializer(data=user)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response({'res': film_serializer.data}, status=status.HTTP_201_CREATED)


class FilmRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = FilmSerializer
    '''
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    '''

    def post(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})

        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

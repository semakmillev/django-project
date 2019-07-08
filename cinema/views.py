import jwt
from django.contrib.auth import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView
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

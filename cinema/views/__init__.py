import jwt
from django.contrib.auth import user_logged_in
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.serializers import jwt_payload_handler, VerifyJSONWebTokenSerializer

from cinema.models import User
from cinema.serializers import FilmSerializer, UserSerializer
from django_project.settings import SECRET_KEY


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

    # @permission_classes((AllowAny,))


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

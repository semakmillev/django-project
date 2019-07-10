import jwt
from django.contrib.auth import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import User
from cinema.serializers import UserSerializer
from rest_framework_jwt.serializers import jwt_payload_handler

from django_project.settings import SECRET_KEY


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'res': serializer.data, 'error': ''}, status=status.HTTP_201_CREATED)


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
            pass
        if user:
            payload = jwt_payload_handler(user)
            token = jwt.encode(payload, SECRET_KEY)
            user_details = {}
            user_details['name'] = user.user_name
            user_details['token'] = token
            user_details['user_id'] = user.id
            user_logged_in.send(sender=user.__class__,
                                request=request, user=user)
            return Response({'res': user_details, 'error': ''}, status=status.HTTP_200_OK)
        else:
            res = {'res': '',
                   'error': 'can not authenticate with the given credentials or the account has been deactivated'}
            return Response(res, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        res = {'res': '', 'error': 'please provide a email and a password'}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

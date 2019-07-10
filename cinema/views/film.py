from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models.film import Film
from cinema.models.user import User
from cinema.serializers import FilmSerializer


@api_view(["POST", ])
def add_film(request):
    serializer = FilmSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'res': serializer.data, 'error': ''}, status=status.HTTP_201_CREATED)
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
        if 'id' in self.kwargs:
            id = self.kwargs['id']
            return Film.objects.filter(id=id)
        else:
            return Film.objects.all()


class CreateFilmAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # user = request.user
        user = User.objects.get(email=request.user)
        if user.user_role != "admin":
            return Response({'message': 'you are not allowed to do it'}, status=status.HTTP_403_FORBIDDEN)

        try:
            film = Film.objects.get(id=request.data['id']) if 'id' in request.data else None
        except ObjectDoesNotExist as ex:
            return Response({'res': '', 'error_message': 'Film not found'}, status=status.HTTP_200_OK)
        film_serializer = FilmSerializer(data=request.data)
        film_serializer.is_valid(raise_exception=True)
        if film is None:
            film_serializer.create(request.data)
            film_serializer.save()
        else:
            film_serializer.update(film, request.data)
        return Response({'res': film_serializer.data, 'error': ''}, status=status.HTTP_201_CREATED)

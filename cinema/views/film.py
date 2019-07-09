from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cinema.models import Film, User
from cinema.serializers import FilmSerializer


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
        return Response({'res': film_serializer.data}, status=status.HTTP_201_CREATED)

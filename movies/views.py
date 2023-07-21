from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Movie, Genre
from .seralizers import MovieSerializer, GenreSerializerCreating, LoginSerializer, RegisterSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication
from .permissions import IsAdminOrReadOnly
from .helping_functions import search_movie_by_key


class Register(APIView):
    """  register new user and create token """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            # create user and handles the password hashing:
            user = User.objects.create_user(**serializer.data)
            # create token:
            Token.objects.create(user=user)
            return Response(serializer.data)
        return Response(serializer.errors)


class Login(APIView):
    """ login user and get his token """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get('username')
            password = serializer.data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                data = {'token': str(token), 'username': username}
                return Response(data)
        return Response(serializer.errors)


class MoviesListCreate(APIView):
    """ get, post for movie """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        """ list al movies """
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ create new movie object if valid """
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class MovieDetailsEditDelete(APIView):
    """ get, put, delete for movie """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk: int):
        """ get movie details by id """
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk: int):
        """ change movie details by id """
        movie = Movie.objects.get(pk=pk)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk: int):
        """ delete movie details by id """
        try:
            movie = Movie.objects.get(pk=pk)
            movie.delete()
            return Response(status=204)
        except Movie.DoesNotExist:
            return Response({"error": "genre does not exist"}, status=404)


class SearchMovie(APIView):
    """ search movie with different keys from query params
        default permission: only authenticated users
     """
    def get(self, request):
        search_result = search_movie_by_key(request)
        return search_result


class GetCreateMovieGenres(APIView):
    """ get, post for genre """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        """ get all genres """
        genres = Genre.objects.all()
        serializer = GenreSerializerCreating(genres, many=True)
        return Response(serializer.data)

    def post(self, request):
        """ create new genre """
        genre = request.data
        serializer = GenreSerializerCreating(data=genre)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class GenreDetailsEditDelete(APIView):
    """ get, put, delete for genre """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, genre: str):
        """ get genre details by name """
        genre = Genre.objects.get(genre=genre)
        serializer = GenreSerializerCreating(genre)
        return Response(serializer.data)

    def put(self, request, genre: str):
        """ change genre details by name """
        genre = Genre.objects.get(genre=genre)
        serializer = GenreSerializerCreating(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, genre: str):
        """ delete genre by name """
        try:
            genre = Genre.objects.get(genre=genre)
            genre.delete()
            return Response(status=204)
        except Genre.DoesNotExist:
            return Response({"error": "genre does not exist"}, status=404)
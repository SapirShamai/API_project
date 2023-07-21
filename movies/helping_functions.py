from .models import Movie
from .seralizers import MovieSerializer
from rest_framework.response import Response


def search_movie_by_key(request):
    """ checking if the keys title/genre/director/cast are in the request
     preform a search accordingly."""

    if 'title' in request.GET:
        matching_movies = Movie.search_by_title(request.GET.get('title'))
        serializer = MovieSerializer(matching_movies, many=True)
        return Response(serializer.data)
    elif 'genre' in request.GET:
        matching_movies = Movie.search_by_genre(request.GET.get('genre'))
        serializer = MovieSerializer(matching_movies, many=True)
        return Response(serializer.data)
    elif 'director' in request.GET:
        matching_movies = Movie.search_by_director(request.GET.get('director'))
        serializer = MovieSerializer(matching_movies, many=True)
        return Response(serializer.data)
    elif 'actor' in request.GET:
        matching_movies = Movie.search_by_actor(request.GET.get('actor'))
        serializer = MovieSerializer(matching_movies, many=True)
        return Response(serializer.data)

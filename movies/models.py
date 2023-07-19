from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=255)

    def __str__(self):
        return self.genre


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.ManyToManyField(Genre)
    director = models.CharField(max_length=255)
    cast = models.TextField()

    def __str__(self):
        return self.title

    @staticmethod
    def search_by_title(title: str):
        """ search movie by the title or part of the title, return list of movies """
        movies = Movie.objects.all()
        title = title.replace(' ', '').lower()
        matching_movies = []
        for movie in movies:
            if title in movie.title.replace(' ', '').lower():
                matching_movies.append(movie)
        return matching_movies

    @staticmethod
    def search_by_genre(genre: str):
        """ search movie by genre """
        movies = Movie.objects.all()
        matching_movies = []
        for movie in movies:
            for qs in movie.genre.all():
                if genre in qs.genre:
                    matching_movies.append(movie)
        return matching_movies



    @staticmethod
    def search_by_director(director: str):
        """ search movie by director """
        movies = Movie.objects.all()
        director = director.replace(' ', '').lower()
        matching_movies = []
        for movie in movies:
            if director in movie.director.replace(' ', '').lower():
                matching_movies.append(movie)
        return matching_movies

    @staticmethod
    def search_by_actor(actor: str):
        """ search movie by actor in the cast attribute"""
        movies = Movie.objects.all()
        actor = actor.replace(' ', '').lower()
        matching_movies = []
        for movie in movies:
            if actor in movie.cast.replace(' ', '').lower():
                matching_movies.append(movie)
        return matching_movies




from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Movie, Genre
from datetime import date


class RegisterSerializer(serializers.Serializer):
    """ register serializer """
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=255, required=False)
    last_name = serializers.CharField(max_length=255, required=False)


class LoginSerializer(serializers.Serializer):
    """ login serializer """
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class UniqueGenreValidator:
    """ validate genre name is unique """
    def __call__(self, value):
        if Genre.objects.filter(genre=value).exists():
            raise ValidationError('Genre with this title already exists')


class GenreSerializerCreating(serializers.ModelSerializer):
    """ genre serializer with validator"""
    genre = serializers.CharField(validators=[UniqueGenreValidator()])

    class Meta:
        model = Genre
        fields = '__all__'


class GenreSerializerAdding(serializers.ModelSerializer):
    """ genre serializer """
    class Meta:
        model = Genre
        fields = '__all__'


class DateValidation:
    """ validate date is not from future """
    def __call__(self, value):
        if value > date.today():
            raise ValidationError('Date can not be from the future')


class MovieSerializer(serializers.ModelSerializer):
    """ movie serializer for all requests except PUT"""
    release_date = serializers.DateField(validators=[DateValidation()])
    genre = GenreSerializerAdding(many=True)

    class Meta:
        model = Movie
        fields = '__all__'

    def create(self, data: dict):
        """ create the Movie object with genres object if valid """
        try:
            # validating the title:
            title = data['title']
            if Movie.objects.filter(title=title).exists():
                raise ValidationError('Title already exists')
            genres_data = data.pop('genre')  # remove genre from data to clean the genre data
            movie = Movie.objects.create(**data)
            for genre in genres_data:
                genre_name = genre['genre']
                genre_object = Genre.objects.get(genre=genre_name)
                movie.genre.add(genre_object)
            return movie
        except Genre.DoesNotExist:
            raise ValueError('Genre is invalid')

    def update(self, instance, validated_data):
        """ update the Movie object with genres if valid """
        try:
            # validating the title:
            title = validated_data["title"]
            existing_movie = Movie.objects.filter(title=title)
            if existing_movie.exists() and existing_movie[0].id != instance.id:
                raise ValidationError('Title already exists')
            genres_data = validated_data.pop('genre')   # remove genre from data to clean the genre data
            instance = super().update(instance, validated_data)
            for genre_data in genres_data:
                genre_name = genre_data['genre']
                genre = Genre.objects.get(genre=genre_name)
                instance.genre.add(genre)
            return instance
        except Genre.DoesNotExist:
            return {"error": "genre is invalid"}



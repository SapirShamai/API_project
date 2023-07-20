from django.test import TestCase
from .seralizers import MovieSerializer, RegisterSerializer, LoginSerializer
from .models import Movie
from django.urls import reverse
from rest_framework.test import APIClient


class MovieTest(TestCase):

    def setUp(self) -> None:

        self.valid_user = {
            "username": "test_valid_user",
            "password": 123,
            "email": "test@test.com"
        }
        self.invalid_user = {
            "username": "test_valid_user",
            "password": 123,
        }

        self.client = APIClient()
        self.client.force_authenticate(self.valid_user)

        self.valid_movie_data = {
            "title": "test title",
            "release_date": "2023-6-14",
            "genre": [
                {"genre": "drama"}
            ],
            "description": "test description",
            "director": "test director",
            "cast": "test actors"
        }
        self.invalid_date_movie_data = {
            "title": "test title",
            "release_date": "2024-6-14",
            "genre": [
                {"genre": "drama"}
            ],
            "description": "test description",
            "director": "test director",
            "cast": "test actors"
        }
        self.invalid_title_movie_data = {
            "release_date": "2023-6-14",
            "genre": [
                {"genre": "drama"}
            ],
            "description": "test description",
            "director": "test director",
            "cast": "test actors"
        }

    def test_movie_valid(self):
        serializer = MovieSerializer(data=self.valid_movie_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.initial_data['title'], 'test title')

    def test_movie_date_invalid(self):
        serializer = MovieSerializer(data=self.invalid_date_movie_data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.data, self.invalid_date_movie_data)

    def test_movie_title_invalid(self):
        serializer = MovieSerializer(data=self.invalid_title_movie_data)
        self.assertFalse(serializer.is_valid())
        self.assertNotIn('title', self.invalid_title_movie_data)

    def test_valid_register_serializer(self):
        serializer = RegisterSerializer(data=self.valid_user)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(str(self.valid_user['password']), serializer.data['password'])

    def test_invalid_user_register(self):
        serializer = RegisterSerializer(data=self.invalid_user)
        self.assertFalse(serializer.is_valid())
        self.assertNotIn('email', self.invalid_user)

    def test_login(self):
        serializer = LoginSerializer(data=self.valid_user)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.data['username'], self.valid_user['username'])

    def tet_movie_details(self):
        movie = Movie.objects.create(**self.valid_movie_data)
        url = reverse('movies:movie_details')
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)

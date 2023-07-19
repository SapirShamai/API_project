from django.urls import path
from .views import MoviesListCreate, MovieDetailsEditDelete, \
    SearchMovie, GetCreateMovieGenres, GenreDetailsEditDelete, Register, Login
app_name = 'movies'


urlpatterns = [
    path('movies', MoviesListCreate.as_view(), name='list_movies'),
    path('movie/<int:pk>/', MovieDetailsEditDelete.as_view(), name='movie_details'),
    path('movie/search/', SearchMovie.as_view(), name='search_movie'),
    path('movie/genres/', GetCreateMovieGenres.as_view(), name='movie_genres'),
    path('movie/genres/<str:genre>', GenreDetailsEditDelete.as_view(), name='genre_details'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),

]

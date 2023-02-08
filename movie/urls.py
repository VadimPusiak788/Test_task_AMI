from django.urls import path

from movie.views import GenresView, MovieDetailView, MoviesView


urlpatterns = [
    path("genres/", GenresView.as_view(), name="genres"),
    path("movies/<int:pk>", MovieDetailView.as_view(), name="detail_movie"),
    path("movies/", MoviesView.as_view(), name="movies"),
]

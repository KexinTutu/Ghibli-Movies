from django.conf.urls import url

from ghibli_movies.apps.movie.views import MovieListAPIView


urlpatterns = [
    url(r'^movies', MovieListAPIView.as_view()),
]
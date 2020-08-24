import requests
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


GHIBLI_API_URL = 'https://ghibliapi.herokuapp.com'
ENDPOINTS = {
    'FILM': 'films',
    'PEOPLE': 'people'
}

class MovieListAPIView(APIView):

    @method_decorator(cache_page(60))
    def get(self, requests, *args, **kwargs):
        try:
            people = self.get_ghibli_api(ENDPOINTS['PEOPLE'])
            movies = self.get_ghibli_api(ENDPOINTS['FILM'])
        except Exception as exception:
            return Response({
                'detail': u'%s' % exception,
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        movies_with_people = self.get_movies_with_people(movies, people)
        return Response(movies_with_people)

    def get_movies_with_people(self, movies, people):
        for movie in movies:
            movie['new_people'] = []
            for person in people:
                if movie['url'] in person['films']:
                    movie['new_people'].append(person)
        return movies

    def get_ghibli_api(self, endpoint):
        url = '%s/%s' % (GHIBLI_API_URL, endpoint)
        try:
            response = requests.get(url)
        except requests.RequestException:
            raise Exception('Ghibli api exception')

        if response.status_code != 200:
            raise Exception('Ghibli api exception')
        return response.json()

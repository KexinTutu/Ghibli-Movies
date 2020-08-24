from unittest import mock

from django.test import TestCase
from django.test.client import RequestFactory
from rest_framework import status

from ghibli_movies.apps.movie.views import MovieListAPIView


class MovieTests(TestCase):

    def setUp(self, *args, **kwargs):
        people_json = [{
            "id": "c491755a-407d-4d6e-b58a-240ec78b5061",
            "name": "Chibi Totoro",
            "gender": "NA",
            "age": "",
            "eye_color": "Black",
            "hair_color": "White",
            "films": [
                "https://ghibliapi.herokuapp.com/films/58611129-2dbc-4a81-a72f-77ddfc1b1b49"
            ],
            "species": "https://ghibliapi.herokuapp.com/species/74b7f547-1577-4430-806c-c358c8b6bcf5",
            "url": "https://ghibliapi.herokuapp.com/people/d39deecb-2bd0-4770-8b45-485f26e1381f"
        },{
            "id": "7151abc6-1a9e-4e6a-9711-ddb50ea572ec",
            "name": "Jiji",
            "gender": "Male",
            "age": "NA",
            "eye_color": "Black",
            "hair_color": "Black",
            "films": [
                "https://ghibliapi.herokuapp.com/films/ea660b10-85c4-4ae3-8a5f-41cea3648e3e"
            ],
            "species": "https://ghibliapi.herokuapp.com/species/603428ba-8a86-4b0b-a9f1-65df6abef3d3",
            "url": "https://ghibliapi.herokuapp.com/people/7151abc6-1a9e-4e6a-9711-ddb50ea572ec"
        }]
        movie_json = [{
            "id": "58611129-2dbc-4a81-a72f-77ddfc1b1b49",
            "title": "My Neighbor Totoro",
            "description": "Two sisters move to the country with their father in order to be closer to their hospitalized mother, and discover the surrounding trees are inhabited by Totoros, magical spirits of the forest. When the youngest runs away from home, the older sister seeks help from the spirits to find her.",
            "director": "Hayao Miyazaki",
            "producer": "Hayao Miyazaki",
            "release_date": "1988",
            "rt_score": "93",
            "people": [
              "https://ghibliapi.herokuapp.com/people/08ffbce4-7f94-476a-95bc-76d3c3969c19",
              "https://ghibliapi.herokuapp.com/people/0f8ef701-b4c7-4f15-bd15-368c7fe38d0a"
            ],
            "species": [
              "https://ghibliapi.herokuapp.com/species/af3910a6-429f-4c74-9ad5-dfe1c4aa04f2",
            ],
            "locations": [
              "https://ghibliapi.herokuapp.com/locations/"
            ],
            "vehicles": [
              "https://ghibliapi.herokuapp.com/vehicles/"
            ],
            "url": "https://ghibliapi.herokuapp.com/films/58611129-2dbc-4a81-a72f-77ddfc1b1b49"
        },]
        self.people = people_json
        self.movies = movie_json

    

    def test_get_movie_list(self):
        def get_api(*args):
            if args[0] == 'people':
                return self.people
            elif args[0] == 'films':
                return self.movies
        with mock.patch.object(MovieListAPIView, 'get_ghibli_api', side_effect=get_api):
            response = self.client.get('/movies')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['content-type'], 'application/json')
            self.assertEqual(
                response.json()[0]['new_people'],
                list(filter(lambda person: person['name'] == 'Chibi Totoro', self.people))
            )

    @mock.patch.object(MovieListAPIView, 'get_ghibli_api')
    def test_get_movie_list_exception(self, mock_ghibli_api):
        mock_ghibli_api.side_effect = Exception('test exception')
        response = self.client.get('/movies')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response['content-type'], 'application/json')
        self.assertEqual(response.json(), {"detail": "test exception"})

    @mock.patch('ghibli_movies.apps.movie.views.requests.get')
    def test_get_ghibli_api_200(self, mock_get):
        request = RequestFactory().get('/test')
        view = MovieListAPIView(request=request)

        mock_response = mock.Mock()
        mock_response.json.return_value = self.people
        mock_response.status_code = 200

        mock_get.return_value = mock_response
        result = view.get_ghibli_api('people')
        self.assertEqual(result, self.people)
    
    @mock.patch('ghibli_movies.apps.movie.views.requests.get')
    def test_get_ghibli_api_400(self, mock_get):
        request = RequestFactory().get('/test')
        view = MovieListAPIView(request=request)
        mock_response = mock.Mock()
        mock_response.json.return_value = {}
        mock_response.status_code = 400

        mock_get.return_value = mock_response
        with self.assertRaises(Exception):
            view.get_ghibli_api('people')

    def test_get_people_of_movie(self):
        request = RequestFactory().get('/test')
        view = MovieListAPIView(request=request)

        result = view.get_movies_with_people(self.movies, self.people)
        self.assertEqual(
            result[0]['new_people'],
            list(filter(lambda person: person['name'] == 'Chibi Totoro', self.people))
        )
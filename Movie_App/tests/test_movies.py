# Movie_App/tests/test_movies.py
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from Movie_App.models import Movie

User = get_user_model()


class MovieCRUDTest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='123'
        )
        self.client = APIClient()
        response = self.client.post(reverse('jwt-create'), {
            'username': 'admin',
            'password': '123'
        })
        self.assertEqual(response.status_code, 200)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.list_url = reverse('movie-list')
        self.movie_data = {
            'title': 'Test Movie',
            'release_date': '2023-01-01',
            'duration': 120
        }

    def test_create_movie(self):
        response = self.client.post(self.list_url, self.movie_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_movie_list(self):
        Movie.objects.create(**self.movie_data)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_movie(self):
        movie = Movie.objects.create(**self.movie_data)
        url = reverse('movie-detail', args=[movie.id])
        response = self.client.patch(url, {'title': 'Updated'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movie.refresh_from_db()
        self.assertEqual(movie.title, 'Updated')

    def test_delete_movie(self):
        movie = Movie.objects.create(**self.movie_data)
        url = reverse('movie-detail', args=[movie.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
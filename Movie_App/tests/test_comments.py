from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from Movie_App.models import Movie, Comment

User = get_user_model()


class CommentCRUDTest(APITestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin', email='admin@test.com', password='123')
        self.user = User.objects.create_user(
            username='user123',
            email='user@test.com',
            password='123'
        )
        self.movie = Movie.objects.create(title='Film', release_date='2023-01-01', duration=100)

        self.client = APIClient()
        response = self.client.post(reverse('jwt-create'), {
            'username': 'user123',
            'password': '123'
        })
        self.assertEqual(response.status_code, 200)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.list_url = reverse('comment-list')
        self.comment_data = {'movie': self.movie.id, 'text': 'Good!'}

    def test_create_comment(self):
        response = self.client.post(self.list_url, self.comment_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_read_comment_list(self):
        Comment.objects.create(movie=self.movie, author=self.user, text='Hi')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_comment(self):
        comment = Comment.objects.create(movie=self.movie, author=self.user, text='Old')
        url = reverse('comment-detail', args=[comment.id])
        response = self.client.patch(url, {'text': 'New'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.text, 'New')

    def test_delete_comment(self):
        comment = Comment.objects.create(movie=self.movie, author=self.user, text='Del')
        url = reverse('comment-detail', args=[comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from posts.models import Post, Like
from accounts.models import CustomUser

class PostLikeTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(author=self.user, title="Test Post", content="This is a test post")
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')

    def test_like_post(self):
        url = reverse('post-like', kwargs={'pk': self.post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.post.likes.count(), 1)

    def test_unlike_post(self):
        Like.objects.create(user=self.user, post=self.post)
        url = reverse('post-unlike', kwargs={'pk': self.post.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.post.likes.count(), 0)
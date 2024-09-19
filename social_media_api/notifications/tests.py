from django.test import TestCase

# Create your tests here.

from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from notifications.models import Notification
from posts.models import Post
from accounts.models import CustomUser

class NotificationTests(APITestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(username='user1', password='password1')
        self.user2 = CustomUser.objects.create_user(username='user2', password='password2')
        self.post = Post.objects.create(author=self.user1, title="Post Title", content="Post content")
        self.client = APIClient()

    def test_like_post_creates_notification(self):
        # Simulate user2 liking user1's post
        self.client.login(username='user2', password='password2')
        url = reverse('post-like', kwargs={'pk': self.post.pk})
        self.client.post(url)

        # Check if notification was created for user1
        notification = Notification.objects.get

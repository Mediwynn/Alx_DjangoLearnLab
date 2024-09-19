from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions, filters, generics, status
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


class PostPagination(PageNumberPagination):
    page_size = 5

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user

        # Check if the user has already liked the post
        like, created = Like.objects.get_or_create(post=post, user=user)

        if not created:
            return Response({'message': 'Already liked'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a notification for the post's author
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb='liked your post',
            target=post,
        )

        return Response({'message': 'Post liked'}, status=status.HTTP_200_OK)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        post = Post.objects.get(pk=pk)
        user = request.user

        like = Like.objects.filter(post=post, user=user).first()
        if like:
            like.delete()
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)

        return Response({'message': 'You have not liked this post'}, status=status.HTTP_400_BAD_REQUEST)

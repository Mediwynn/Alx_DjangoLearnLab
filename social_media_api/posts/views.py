from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions, filters, generics, status
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

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

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        # Fetch the post by ID, if it doesn't exist, return 404
        post = get_object_or_404(Post, pk=pk)

        # Get or create a like object for the user-post relationship
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            # If the like already exists, return a message saying the post is already liked
            return Response({"message": "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a notification for the post author when the post is liked
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )

        # Return a success message
        return Response({"message": "Post liked successfully"}, status=status.HTTP_201_CREATED)

class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk, *args, **kwargs):
        # Fetch the post by ID, if it doesn't exist, return 404
        post = get_object_or_404(Post, pk=pk)

        # Try to fetch the like object
        like = Like.objects.filter(user=request.user, post=post).first()
        
        if like:
            # If the like exists, delete it and return success response
            like.delete()
            return Response({"message": "Post unliked successfully"}, status=status.HTTP_200_OK)
        else:
            # If the like doesn't exist, return an error response
            return Response({"message": "You haven't liked this post yet!"}, status=status.HTTP_400_BAD_REQUEST)


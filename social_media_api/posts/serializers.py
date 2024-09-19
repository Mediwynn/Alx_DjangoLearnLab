from rest_framework import serializers
from .models import Post, Comment, Like
from .serializers import CommentSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at', 'updated_at']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')  # Read-only author field (username)
    comments = CommentSerializer(many=True, read_only=True)  # Nested serializer for comments
    likes_count = serializers.SerializerMethodField()  # Method field for likes count

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'likes_count', 'comments']

    # Method to get the count of likes on a post
    def get_likes_count(self, obj):
        return obj.likes.count()


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
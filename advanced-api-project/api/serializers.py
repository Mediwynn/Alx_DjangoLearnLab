from rest_framework import serializers
from .models import Book, Author
from time import timezone

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        if value > timezone.now().year:
            raise serializers.ValidationError("The publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
        
# The BookSerializer includes custom validation to ensure publication_year is not in the future.
# The AuthorSerializer nests the BookSerializer to display related books for each author.
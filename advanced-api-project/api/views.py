from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


# BookListView handles GET (list all books) and POST (create a new book).
# Read access is open to all, but creating a new book requires authentication.
class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# BookDetailView handles GET (retrieve a book), PUT/PATCH (update a book), and DELETE (remove a book).
# Only authenticated users can modify or delete books, but all users can view them.
class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Custom behavior before saving a new book
        serializer.save()

    def perform_update(self, serializer):
        # Custom behavior before updating an existing book
        serializer.save()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()






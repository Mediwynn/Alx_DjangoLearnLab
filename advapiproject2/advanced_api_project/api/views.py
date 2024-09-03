from django.shortcuts import render

# Create your views here.

from rest_framework import generics, filters
from api.models import Book
from api.serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# BookListView handles GET (list all books) and POST (create a new book).
# Read access is open to all, but creating a new book requires authentication.
# ListView: Handles retrieving all books
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'author__name', 'publication_year']
    search_fields = ['title', 'author__name']
    ordering_fields = ['title', 'publication_year']

# BookDetailView handles GET (retrieve a book), PUT/PATCH (update a book), and DELETE (remove a book).
# Only authenticated users can modify or delete books, but all users can view them.
# DetailView: Handles retrieving a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# CreateView: Handles adding a new book
class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# UpdateView: Handles modifying an existing book
class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# DeleteView: Handles removing a book
class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]



# BookListView handles retrieving a list of books with advanced querying capabilities.
# Users can filter by title, author name, and publication year.
# They can also search across the title and author fields and order results by title or publication year.




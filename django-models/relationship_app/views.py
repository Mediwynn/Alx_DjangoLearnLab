from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Book
from django.views.generic import DetailView
from .models import Library

def list_books(request):
    # Query all books from the database
    books = Book.objects.all()
    
    # Generate a list of book titles and authors
    book_list = "\n".join([f"{book.title} by {book.author.name}" for book in books])
    
    # Return the list as a plain text response
    return HttpResponse(book_list, content_type="text/plain")



class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the list of books in the library to the context
        context['books'] = self.object.books.all()  # Assuming 'books' is the related name for the ManyToManyField
        return context
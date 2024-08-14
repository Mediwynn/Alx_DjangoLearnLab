from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from bookshelf.models import Book
from django.views.generic import DetailView
from relationship_app.models import Library

def list_books(request):
    # Query all books from the database
    books = Book.objects.select_related('author').all()
    
    # Pass the books to the template
    context = {
        'books': books,
    }
    
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

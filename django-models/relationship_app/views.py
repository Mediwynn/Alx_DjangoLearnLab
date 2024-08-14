from django.shortcuts import render

# Create your views here.
from .models import Book
from django.views.generic import DetailView
from .models import Library
from django.views.generic.detail import DetailView

def list_books(request):
    # Query all books from the database
    books = Book.objects.all()
    
    # Pass the books to the template
    context = {
        'books': books,
    }
    
    return render(request, 'relationship_app/list_books.html', context)



class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the list of books in the library to the context
        context['books'] = self.object.books.all()  # Assuming 'books' is the related name for the ManyToManyField
        return context
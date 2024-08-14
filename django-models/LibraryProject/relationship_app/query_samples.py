import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        for book in books:
            print(f'Book Title: {book.title}')
    except Author.DoesNotExist:
        print(f'No author found with name {author_name}')

def list_all_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        for book in books:
            print(f'Book Title: {book.title}')
    except Library.DoesNotExist:
        print(f'No library found with name {library_name}')

def retrieve_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f'Librarian Name: {librarian.name}')
    except Library.DoesNotExist:
        print(f'No library found with name {library_name}')
    except Librarian.DoesNotExist:
        print(f'No librarian found for library {library_name}')

if __name__ == '__main__':
    # Example queries
    print('Books by J.K. Rowling:')
    query_all_books_by_author('J.K. Rowling')
    
    print('\nBooks in Central Library:')
    list_all_books_in_library('Central Library')
    
    print('\nLibrarian for Central Library:')
    retrieve_librarian_for_library('Central Library')

# relationship_app/query_samples.py

from relationship_app.models import Author, Book, Library, Librarian

def query_books_by_author(Author):
    """
    Query all books by a specific author.
    :param Author: The name of the author.
    :return: QuerySet of books written by the specified author.
    """
    books_by_author = Book.objects.filter(author__name=Author)
    return books_by_author

def list_books_in_library(library_name):
    """
    List all books in a specific library.
    :param library_name: The name of the library.
    :return: QuerySet of books available in the specified library.
    """
    try:
        library = Library.objects.get(name=library_name)
        books_in_library = library.books.all()
        return books_in_library
    except Library.DoesNotExist:
        return None

def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a specific library.
    :param library_name: The name of the library.
    :return: The Librarian object for the specified library.
    """
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # Assuming the related_name is 'librarian'
        return librarian
    except Library.DoesNotExist:
        return None

if __name__ == "__main__":
    # Sample usage
    #Author = "J.K. Rowling"
    #library_name = "Central Library"

    # Query books by a specific author
    books = query_books_by_author(Author)
    print(f"Books by {Author}:")
    for book in books:
        print(f"- {book.title}")

    # List all books in a specific library
    books_in_library = list_books_in_library(library_name)
    if books_in_library is not None:
        print(f"\nBooks in {library_name}:")
        for book in books_in_library:
            print(f"- {book.title}")
    else:
        print(f"\nLibrary '{library_name}' does not exist.")

    # Retrieve the librarian for a specific library
    librarian = retrieve_librarian_for_library(library_name)
    if librarian is not None:
        print(f"\nLibrarian of {library_name}: {librarian.name}")
    else:
        print(f"\nNo librarian found for '{library_name}' or library does not exist.")

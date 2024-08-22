from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .forms import BookForm, ExampleForm
from .models import Book

# View Books
@permission_required('bookshelf.can_view', raise_exception=True)
def view_books(request):
    """
    Retrieve and display all books.
    Access is restricted to users with 'bookshelf.can_view' permission.
    """
    books = Book.objects.all()  # Retrieve all books safely using Django ORM
    return render(request, 'bookshelf/book_list.html', {'books': books})

# Create Book
@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    """
    Handle creation of a new book.
    Access is restricted to users with 'bookshelf.can_create' permission.
    """
    if request.method == 'POST':
        form = BookForm(request.POST)  # Instantiate form with POST data
        if form.is_valid():  # Validate form data
            form.save()  # Save new book to the database
            return redirect('view_books')  # Redirect to book list view
    else:
        form = BookForm()  # Instantiate an empty form for GET requests
    
    return render(request, 'bookshelf/book_form.html', {'form': form})

# Edit Book
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    """
    Handle editing of an existing book.
    Access is restricted to users with 'bookshelf.can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)  # Retrieve the book or return a 404 error
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)  # Instantiate form with POST data and book instance
        if form.is_valid():  # Validate form data
            form.save()  # Save changes to the book
            return redirect('view_books')  # Redirect to book list view
    else:
        form = BookForm(instance=book)  # Instantiate form with existing book data for GET requests
    
    return render(request, 'bookshelf/book_form.html', {'form': form})

# Delete Book
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    """
    Handle deletion of a book.
    Access is restricted to users with 'bookshelf.can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)  # Retrieve the book or return a 404 error
    
    if request.method == 'POST':
        book.delete()  # Delete the book from the database
        return redirect('view_books')  # Redirect to book list view
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# Example View using ExampleForm
@permission_required('bookshelf.can_use_example_form', raise_exception=True)
def example_view(request):
    """
    Handle form submission for ExampleForm.
    Access is restricted to users with 'bookshelf.can_use_example_form' permission.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)  # Instantiate form with POST data
        if form.is_valid():  # Validate form data
            form.save()  # Handle form submission logic (e.g., saving data)
            return redirect('success_page')  # Redirect to a success page
    else:
        form = ExampleForm()  # Instantiate an empty form for GET requests
    
    return render(request, 'bookshelf/example_form.html', {'form': form})

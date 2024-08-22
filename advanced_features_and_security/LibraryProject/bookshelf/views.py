from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.views.decorators.csrf import csrf_protect
from .models import Book

# View Books
@permission_required('your_app_name.can_view', raise_exception=True)
def view_books(request):
    # Retrieve all books safely using Django ORM
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

# Create Book
@csrf_protect  # Ensure CSRF protection for this view
@permission_required('your_app_name.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        # Validate input
        if title and author and publication_year:
            # Use Django ORM to create the book safely
            Book.objects.create(title=title, author=author, publication_year=publication_year)
            return redirect('view_books')
    
    return render(request, 'relationship_app/book_form.html')

# Edit Book
@csrf_protect  # Ensure CSRF protection for this view
@permission_required('your_app_name.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        # Validate input
        if title and author and publication_year:
            book.title = title
            book.author = author
            book.publication_year = publication_year
            book.save()  # Use Django ORM to save changes
            return redirect('view_books')
    
    return render(request, 'relationship_app/book_form.html', {'book': book})

# Delete Book
@csrf_protect  # Ensure CSRF protection for this view
@permission_required('your_app_name.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()  # Use Django ORM to delete the book
        return redirect('view_books')
    
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})

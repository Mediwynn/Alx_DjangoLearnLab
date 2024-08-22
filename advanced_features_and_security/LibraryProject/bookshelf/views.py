from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book

# View Books
@permission_required('your_app_name.can_view', raise_exception=True)
def view_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/book_list.html', {'books': books})

# Create Book
@permission_required('your_app_name.can_create', raise_exception=True)
def create_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        if title and author and publication_year:
            Book.objects.create(title=title, author=author, publication_year=publication_year)
            return redirect('view_books')
    return render(request, 'relationship_app/book_form.html')

# Edit Book
@permission_required('your_app_name.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        if book.title and book.author and book.publication_year:
            book.save()
            return redirect('view_books')
    return render(request, 'relationship_app/book_form.html', {'book': book})

# Delete Book
@permission_required('your_app_name.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('view_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})

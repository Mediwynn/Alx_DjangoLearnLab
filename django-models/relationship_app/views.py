from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Book

def list_books(request):
    books = Book.objects.all()
    book_list = '\n'.join([f'Title: {book.title}, Author: {book.author.name}' for book in books])
    return HttpResponse(book_list, content_type='text/plain')

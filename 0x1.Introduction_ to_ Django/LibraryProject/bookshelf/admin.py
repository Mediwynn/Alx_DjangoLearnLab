from django.contrib import admin

# Register your models here.
from .models import Book

admin.site.register(Book)

class BookAdmin(admin.ModelAdmin):
    # Display title, author, and publication_year in the list view
    list_display = ('title', 'author', 'publication_year')
    
    # Add filters for author and publication_year
    list_filter = ('author', 'publication_year')
    
    # Enable search functionality for title and author
    search_fields = ('title', 'author')

# Register the Book model with the custom admin configuration
admin.site.register(Book, BookAdmin)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.
# relationship_app/admin.py

from django.contrib import admin
from .models import Author, Book, Library, Librarian

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('name',)

#@admin.register(Librarian)
#class LibrarianAdmin(admin.ModelAdmin):
    #list_display = ('name', 'library')




class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

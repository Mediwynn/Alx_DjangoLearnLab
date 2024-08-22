from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book  # Import your CustomUser and Book models
from django.utils.translation import gettext_lazy as _

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    # Define the fields to be used in displaying the User model.
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to be used when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'date_of_birth', 'profile_photo', 'password1', 'password2'),
        }),
    )

    # Columns to display in the user list in the admin
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('email',)

# Register the CustomUser model with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# Register the Book model
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    ordering = ('id',)

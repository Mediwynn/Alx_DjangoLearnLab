from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Library, CustomUser, UserProfile  # Import the CustomUser and UserProfile models
from relationship_app.models import Book, Author

# Login View
class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'  # Specify the template for login


# Logout View
class UserLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'  # Specify the template for logout


# User Registration View
class UserRegisterView(CreateView):
    form_class = UserCreationForm  # Specify the form class for registration
    template_name = 'relationship_app/register.html'  # Specify the template for registration
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration

    def form_valid(self, form):
        """If the form is valid, save the user and log them in."""
        user = form.save()
        # Add additional fields to the user model
        user.date_of_birth = self.request.POST.get('date_of_birth')
        user.profile_photo = self.request.FILES.get('profile_photo')
        user.save()
        # Create a UserProfile instance for the user
        UserProfile.objects.create(user=user, role=self.request.POST.get('role'))
        login(self.request, user)  # Log the user in after registration
        return redirect(self.success_url)


# Admin View
def is_admin(user):
    return user.userprofile.role == 'Admin'

@user_passes_test(is_admin)
def admin_view(request):
    """This view is only accessible by users with the 'Admin' role."""
    return render(request, 'relationship_app/admin_view.html')


# Librarian View
def is_librarian(user):
    return user.userprofile.role == 'Librarian'

@user_passes_test(is_librarian)
def librarian_view(request):
    """This view is only accessible by users with the 'Librarian' role."""
    return render(request, 'relationship_app/librarian_view.html')


# Member View
def is_member(user):
    return user.userprofile.role == 'Member'

@user_passes_test(is_member)
def member_view(request):
    """This view is only accessible by users with the 'Member' role."""
    return render(request, 'relationship_app/member_view.html')


# List Books View
class list_books(DetailView):
    model = Library  # Specify the model to be used
    template_name = 'relationship_app/library_detail.html'  # Specify the template for the view
    context_object_name = 'library'  # Name of the context object used in the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()  # Get all books associated with the library
        return context


# Create Book View
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        if title and author_id and publication_year:
            Book.objects.create(title=title, author_id=author_id, publication_year=publication_year)
            return redirect('book_list')  # Redirect to a list of books or another appropriate view
    authors = Author.objects.all()
    return render(request, 'relationship_app/book_form.html', {'authors': authors})

# Update Book View
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author_id = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        if book.title and book.author_id and book.publication_year:
            book.save()
            return redirect('book_list')  # Redirect to a list of books or another appropriate view
    authors = Author.objects.all()
    return render(request, 'relationship_app/book_form.html', {'book': book, 'authors': authors})

# Delete Book View
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')  # Redirect to a list of books or another appropriate view
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})

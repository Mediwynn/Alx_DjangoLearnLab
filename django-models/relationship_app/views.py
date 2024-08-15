from django.shortcuts import render

# Create your views here.
from .models import Book
from django.views.generic import DetailView
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth import login
from django.shortcuts import redirect

def list_books(request):
    # Query all books from the database
    books = Book.objects.all()
    
    # Pass the books to the template
    context = {
        'books': books,
    }
    
    return render(request, 'relationship_app/list_books.html', context)

class LibraryDetailView(DetailView):

    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the list of books in the library to the context
        context['books'] = self.object.books.all()  # Assuming 'books' is the related name for the ManyToManyField
        return context

# Login View
class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'  # Specify the template for login

# Logout View
class UserLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'  # Specify the template for logout

# User Registration View
class UserRegisterView(CreateView):
    form_class = UserCreationForm()  # Specify the form class for registration
    template_name = 'relationship_app/register.html'  # Specify the template for registration
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration

    def form_valid(self, form):
        """If the form is valid, save the user and log them in."""
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)  # Log the user in after registration
        return response

from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from .models import Library  # Import the Library model


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
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)  # Log the user in after registration
        return response


# Admin View
#def is_admin(user):
#    return user.userprofile.role == 'Admin'

#@user_passes_test(is_admin)
#def admin_view(request):
#    """This view is only accessible by users with the 'Admin' role."""
#    return render(request, 'relationship_app/admin_view.html')


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

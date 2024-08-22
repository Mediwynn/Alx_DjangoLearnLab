from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        # Optionally, you can customize widgets and labels here
        widgets = {
            'publication_year': forms.NumberInput(attrs={'placeholder': 'Enter publication year'}),
        }
        labels = {
            'title': 'Book Title',
            'author': 'Author Name',
            'publication_year': 'Year of Publication',
        }

class ExampleForm(forms.Form):
    # Example fields for ExampleForm
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Your Message')

    # Optionally, you can add custom validation methods
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Message is too short.')
        return message

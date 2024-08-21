from django import forms
from django.conf import settings

class ExampleForm(forms.ModelForm):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['username', 'email', 'date_of_birth', 'profile_photo']

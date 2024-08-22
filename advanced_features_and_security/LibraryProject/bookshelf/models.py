from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

# Book model with custom permissions
class Book(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing integer field as primary key
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        ]

    def save(self, *args, **kwargs):
        if not self.id:
            # If no ID is set, set it to the next available integer
            max_id = Book.objects.aggregate(models.Max('id'))['id__max']
            self.id = max_id + 1 if max_id else 1
        super(Book, self).save(*args, **kwargs)

    def __str__(self):
        return f"id={self.id} title= {self.title} author= {self.author} published in the year {self.publication_year}"

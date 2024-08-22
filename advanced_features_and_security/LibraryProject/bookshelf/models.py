from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth=None, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, date_of_birth=None, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password, and superuser privileges.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, date_of_birth, password, **extra_fields)


# Custom User model
class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # Set the custom manager
    objects = CustomUserManager()

    # Specify that the email field should be unique
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


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

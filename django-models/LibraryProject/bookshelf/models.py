from django.db import models

# Create your models here.

class Book(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing integer field as primary key
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.id:
            # If no ID is set, set it to the next available integer
            max_id = Book.objects.aggregate(models.Max('id'))['id__max']
            self.id = max_id + 1 if max_id else 1
        super(Book, self).save(*args, **kwargs)


    def __str__(self):
        return f"id={self.id} title= {self.title} author= {self.author} published in the year {self.publication_year}"
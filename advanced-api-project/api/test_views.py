from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book
from django.contrib.auth.models import User
from rest_framework.test import APIClient

class BookAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.author = Author.objects.create(name='Author Name')
        self.book = Book.objects.create(title='Sample Book', publication_year=2023, author=self.author)
        self.client = APIClient()
        self.client.login(username='testuser', password='password')
        
    def test_create_book(self):
        url = reverse('book-create')
        data = {'title': 'New Book', 'publication_year': 2024, 'author': self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=2).title, 'New Book')

    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Sample Book')

    def test_update_book(self):
        url = reverse('book-update', args=[self.book.id])
        data = {'title': 'Updated Book', 'publication_year': 2023, 'author': self.author.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        url = reverse('book-delete', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_title(self):
        url = f"{reverse('book-list')}?title=Sample Book"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Sample Book')

    def test_search_books(self):
        url = f"{reverse('book-list')}?search=Sample"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Sample Book')

    def test_order_books_by_publication_year(self):
        Book.objects.create(title='Another Book', publication_year=2022, author=self.author)
        url = f"{reverse('book-list')}?ordering=publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2022)
        self.assertEqual(response.data[1]['publication_year'], 2023)

    def test_permissions_for_create_update_delete(self):
        self.client.logout()
        create_url = reverse('book-create')
        update_url = reverse('book-update', args=[self.book.id])
        delete_url = reverse('book-delete', args=[self.book.id])

        # Test create without authentication
        response = self.client.post(create_url, {'title': 'Unauthorized Book', 'publication_year': 2024, 'author': self.author.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test update without authentication
        response = self.client.put(update_url, {'title': 'Unauthorized Update', 'publication_year': 2023, 'author': self.author.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test delete without authentication
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

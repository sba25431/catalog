from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import Book

class BookViewTest(APITestCase):
    def test_get_books(self):
        Book.objects.create(
            title="Test Book", 
            author="Test Author", 
            isbn="1234567890123", 
            published_date="2026-01-01"
        )
        url = reverse('books')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['title'], "Test Book")
        self.assertEqual(response.data[0]['isbn'], "1234567890123")

    def test_post_book_success(self):
        url = reverse('books')
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "9876543210987",
            "published_date": "2026-02-01"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, "New Book")

    def test_post_book_invalid(self):
        url = reverse('books')
        data = {
            "title": "Invalid Book",
            "author": "Invalid Author"
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, 400)
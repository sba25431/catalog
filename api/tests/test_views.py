from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import Book

class BookViewTest(APITestCase):
    def test_get_books(self):
        # Создаем тестовую книгу в виртуальной БД
        Book.objects.create(
            title="Test Book", author="Test Author", description="Test Desc"
        )

        url = reverse("books")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["title"], "Test Book")
        self.assertEqual(response.data[0]["author"], "Test Author")

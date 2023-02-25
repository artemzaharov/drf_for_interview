
from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer

class BookApiTestCase(APITestCase):

    def setUp(self):
        self.book_1 = Book.objects.create(title="Book test",  price=10.0, author_name="Author 1")
        self.book_2 = Book.objects.create(title="Book test 2",  price=20.0, author_name="Author test 2")
        self.book_3 = Book.objects.create(title="Book test 3 Author 1",  price=30.0, author_name="Author test 3")

    def test_get(self):
        url = reverse('book-list')
        # self.client is a client that can be used to make requests to the API
        response = self.client.get(url)
        # we use BooksSerializer to serialize the data if something changes in the serializers.py we can change it in one place
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(response.status_code, 200)
        # we can use the assertEqual method to compare the response.data with the expected result
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        response = self.client.get(url, data={'search': "Author 1"})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data, response.data)
        print(response.data)
        print(serializer_data)
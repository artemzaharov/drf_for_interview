from django.test import TestCase
from store.models import Book
from store.serializers import BooksSerializer

class BookSerializerTestCase(TestCase):
    def test_serializer(self):
        book_1 = Book.objects.create(title="Book test",  price=10.0)
        book_2 = Book.objects.create(title="Book test 2",  price=20.0)
        data = BooksSerializer([book_1, book_2], many=True).data
        excepted_data = [
            { 
            'id': book_1.id,
            'title': 'Book test',
            'price': '10.00'
            },
            {
            'id': book_2.id,
            'title': 'Book test 2',
            'price': '20.00'
            }
            ]
        self.assertEqual(data, excepted_data)
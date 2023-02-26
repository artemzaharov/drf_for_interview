from django.test import TestCase
from store.models import Book
from store.serializers import BooksSerializer

class BookSerializerTestCase(TestCase):
    def test_serializer(self):
        book_1 = Book.objects.create(title="Book test",  price=10.0, author_name="New Author")
        book_2 = Book.objects.create(title="Book test 2",  price=20.0, author_name="New Author2")
        data = BooksSerializer([book_1, book_2], many=True).data
        excepted_data = [
            { 
            'id': book_1.id,
            'title': 'Book test',
            'price': '10.00',
            'author_name': 'New Author'
            },
            {
            'id': book_2.id,
            'title': 'Book test 2',
            'price': '20.00',
            'author_name': 'New Author2'
            }
            ]
        self.assertEqual(data, excepted_data)
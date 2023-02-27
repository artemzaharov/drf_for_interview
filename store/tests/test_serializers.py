from django.test import TestCase
from store.models import Book
from store.serializers import BooksSerializer
from django.contrib.auth.models import User

class BookSerializerTestCase(TestCase):
    def test_serializer(self):

        self.user = User.objects.create_user(username="test")
        self.client.force_login(user=self.user)


        book_1 = Book.objects.create(title="Book test",  price=10.0, author_name="New Author", owner=self.user)
        book_2 = Book.objects.create(title="Book test 2",  price=20.0, author_name="New Author2", owner=self.user)
        data = BooksSerializer([book_1, book_2], many=True).data
        excepted_data = [
            { 
            'id': book_1.id,
            'title': 'Book test',
            'price': '10.00',
            'author_name': 'New Author',
            "owner": book_1.owner.id,
            },
            {
            'id': book_2.id,
            'title': 'Book test 2',
            'price': '20.00',
            'author_name': 'New Author2',
            "owner": book_2.owner.id,
            }
            ]
        self.assertEqual(data, excepted_data)
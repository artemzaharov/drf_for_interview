from rest_framework.test import APITestCase
from django.urls import reverse
from store.models import Book
from store.serializers import BooksSerializer
import json
from rest_framework import status
from django.contrib.auth.models import User


class BookApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test")
        self.book_1 = Book.objects.create(
            title="Book test", price=10.0, author_name="Author 1", owner=self.user
        )
        self.book_2 = Book.objects.create(
            title="Book test 2", price=20.0, author_name="Author test 2"
        )
        self.book_3 = Book.objects.create(
            title="Book test 3 Author 1", price=30.0, author_name="Author test 3"
        )

    def test_get(self):
        url = reverse("book-list")
        # self.client is a client that can be used to make requests to the API
        response = self.client.get(url)
        # we use BooksSerializer to serialize the data if something changes in the serializers.py we can change it in one place
        serializer_data = BooksSerializer(
            [self.book_1, self.book_2, self.book_3], many=True
        ).data
        self.assertEqual(response.status_code, 200)
        # we can use the assertEqual method to compare the response.data with the expected result
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse("book-list")
        response = self.client.get(url, data={"search": "Author 1"})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(serializer_data, response.data)


    def test_create(self):
        url = reverse("book-list")
        data = {"title": "Book test 4", "price": 40, "author_name": "Author test 4"}
        json_data = json.dumps(data)
        self.client.force_login(user=self.user)
        response = self.client.post(
            url, data=json_data, content_type="application/json"
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Book.objects.count())
        self.assertEqual(self.user, Book.objects.last().owner)

    def test_update(self):
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "title": self.book_1.title,
            "price": 999,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(user=self.user)
        response = self.client.put(url, data=json_data, content_type="application/json")

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # we need to refresh the object from the database to get the updated data
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()
        self.assertEqual(999, Book.objects.get(id=self.book_1.id).price)

    def test_delete(self):
        url = reverse("book-detail", args=(self.book_1.id,))
        self.client.force_login(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(2, Book.objects.count())

    def test_update_not_owner(self):
        self.user2 = User.objects.create_user(username="test2")
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "title": self.book_1.title,
            "price": 999,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(user=self.user2)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(response.data, {"detail": "You do not have permission to perform this action."})
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(10, Book.objects.get(id=self.book_1.id).price)

    def test_update_not_owner_but_staff(self):
        self.user2 = User.objects.create_user(username="test2", is_staff=True)
        url = reverse("book-detail", args=(self.book_1.id,))
        data = {
            "title": self.book_1.title,
            "price": 999,
            "author_name": self.book_1.author_name,
        }
        json_data = json.dumps(data)
        self.client.force_login(user=self.user2)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        self.assertEqual(999, Book.objects.get(id=self.book_1.id).price)
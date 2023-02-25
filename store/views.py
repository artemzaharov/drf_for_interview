from rest_framework.viewsets import ModelViewSet
from .models import Book
from .serializers import BooksSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

# Create your views here.
class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # clean cache of browser if doesn't work
    permission_classes = [IsAuthenticated]
    filterset_fields = ['price']
    search_fields = ['title', 'author_name']
    ordering_fields = ['price', 'author_name'] 

def auth(request):
    return render(request, 'oauth.html')
from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=100)

    def __str__(self):
        return f"ID {self.id} : {self.title}"

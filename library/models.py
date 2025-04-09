from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    total_copies = models.PositiveIntegerField(default=0)
    published_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} borrowed {self.book.title}'

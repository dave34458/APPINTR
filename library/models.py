from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('staff', 'Staff'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=5, choices=ROLE_CHOICES, default='user')

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, blank=True)
    preview_image = models.ImageField(upload_to='book_previews/', null=True, blank=True)

class AvailableBook(models.Model):
    book = models.ForeignKey(Book, related_name="available_books", on_delete=models.CASCADE)
    location = models.CharField(max_length=255)

class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    available_book = models.ForeignKey(AvailableBook, related_name="borrows", on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField(blank=True)

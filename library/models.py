from django.db import models
from django.contrib.auth.models import User


# Book model with details about the book.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'


# AvailableBooks model which will track the availability of a book.
class AvailableBook(models.Model):
    book = models.ForeignKey(Book, related_name="available_books", on_delete=models.CASCADE)
    location = models.CharField(max_length=255)  # Location where the book is available
    available_copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.book.title} available at {self.location}'

    def is_available(self):
        return self.available_copies > 0


# Borrow model that links a book to a user, tracking borrowed books.
class Borrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    available_book = models.ForeignKey(AvailableBook, related_name="borrows", on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} borrowed {self.available_book.book.title} from {self.available_book.location}'


# Review model for users to review books
class Review(models.Model):
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1-5 rating scale
    comment = models.TextField(blank=True)

    def __str__(self):
        return f'Review by {self.user.username} for {self.book.title}'

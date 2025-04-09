from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Book, Borrow, AvailableBook, Review, CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


# Updated BookSerializer to exclude total_copies
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'genre', 'isbn', 'description', 'language']

class AvailableBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableBook
        fields = ['id', 'book', 'location']

# Updated BorrowSerializer to include information about available books
class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id', 'user', 'available_book', 'borrow_date', 'return_date']


# ReviewSerializer for user reviews
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'comment']


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

class BookSerializer(serializers.ModelSerializer):
    is_available = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'published_date',
            'genre', 'isbn', 'description', 'language',
            'preview_image', 'is_available',
        ]

    def get_is_available(self, obj):
        for ab in obj.available_books.all():
            if not ab.borrows.filter(date_returned__isnull=True).exists():
                return True
        return False

class AvailableBookSerializer(serializers.ModelSerializer):
    copy_is_available = serializers.SerializerMethodField()

    class Meta:
        model = AvailableBook
        fields = ['id', 'book', 'location', 'copy_is_available']

    def get_copy_is_available(self, obj):
        # Check if there is at least one available copy of the book based on the get_is_available logic
        if not obj.borrows.filter(date_returned__isnull=True).exists():
            return True
        return False


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ['id', 'user', 'available_book', 'borrow_date', 'return_date', 'date_returned']

    def validate(self, data):
        if self.context['request'].method == 'POST' and Borrow.objects.filter(available_book=data['available_book'], date_returned__isnull=True).exists():
            raise serializers.ValidationError('This book has already been borrowed and not returned yet.')
        return data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'comment']


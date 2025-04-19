from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Book, Borrow, AvailableBook, Review, CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'password']

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


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
        return any(
            not ab.borrows.filter(date_returned__isnull=True).exists()
            for ab in obj.available_books.all()
        )


class AvailableBookReadSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    copy_is_available = serializers.SerializerMethodField()

    class Meta:
        model = AvailableBook
        fields = ['id', 'book', 'location', 'copy_is_available']

    def get_copy_is_available(self, obj):
        return not obj.borrows.filter(date_returned__isnull=True).exists()

class AvailableBookWriteSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = AvailableBook
        fields = ['id', 'book', 'location']


class BorrowReadSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    available_book = AvailableBookReadSerializer(read_only=True)

    class Meta:
        model = Borrow
        fields = ['id', 'user', 'available_book', 'borrow_date', 'return_date', 'date_returned']


class BorrowWriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    available_book = serializers.PrimaryKeyRelatedField(queryset=AvailableBook.objects.all())

    class Meta:
        model = Borrow
        fields = ['id', 'user', 'available_book', 'borrow_date', 'return_date', 'date_returned']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Borrow.objects.filter(
                available_book=data['available_book'],
                date_returned__isnull=True
            ).exists():
                raise serializers.ValidationError('This book is currently borrowed.')
        return data


class ReviewReadSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'comment']

class ReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['book', 'rating', 'comment']


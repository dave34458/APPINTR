from django.contrib import admin
from .models import CustomUser, Book, AvailableBook, Borrow, Review

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('role', 'is_staff', 'is_active')

admin.site.register(CustomUser, CustomUserAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'genre', 'isbn', 'language')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('genre', 'language', 'published_date')

admin.site.register(Book, BookAdmin)

class AvailableBookAdmin(admin.ModelAdmin):
    list_display = ('book', 'location')
    search_fields = ('book__title', 'location')

admin.site.register(AvailableBook, AvailableBookAdmin)

class BorrowAdmin(admin.ModelAdmin):
    list_display = ('user', 'available_book', 'borrow_date', 'return_date', 'date_returned')
    search_fields = ('user__username', 'available_book__book__title')
    list_filter = ('borrow_date', 'return_date')

admin.site.register(Borrow, BorrowAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'rating', 'comment')
    search_fields = ('user__username', 'book__title')
    list_filter = ('rating',)

admin.site.register(Review, ReviewAdmin)

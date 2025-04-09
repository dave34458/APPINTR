from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import BookViewSet, AvailableBookViewSet, BorrowViewSet, ReviewViewSet, RegisterView, LogoutView

# Default router for books and reviews
router = DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet)
router.register(r'availablebooks', AvailableBookViewSet)
router.register(r'borrows', BorrowViewSet)
router.register(r'reviews', ReviewViewSet)

# Nested router for availablebooks under books
books_router = NestedDefaultRouter(router, r'books', lookup='book')
books_router.register(r'availablebooks', AvailableBookViewSet, basename='book-availablebooks')

# Nested router for borrows under availablebooks
available_books_router = NestedDefaultRouter(books_router, r'availablebooks', lookup='available_book')
available_books_router.register(r'borrows', BorrowViewSet, basename='availablebook-borrows')

# Nested router for reviews under books
books_router.register(r'reviews', ReviewViewSet, basename='book-reviews')

urlpatterns = [
    path('auth/users', RegisterView.as_view()),
    path('auth/sessions', obtain_auth_token),
    path('auth/logout', LogoutView.as_view()),
    path('', include(router.urls)),
    path('', include(books_router.urls)),
    path('', include(available_books_router.urls)),
]

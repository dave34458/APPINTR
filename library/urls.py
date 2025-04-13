from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_nested import routers
from .views import (
    BookViewSet,
    AvailableBookViewSet,
    BorrowViewSet,
    ReviewViewSet,
    RegisterView,
    LogoutView,
    UserViewSet
)

# Base router for flat resources (flat routes like /api/availablebooks/)
router = routers.DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet, basename='book')
router.register(r'availablebooks', AvailableBookViewSet, basename='availablebook-flat')  # Ensure this is set
router.register(r'borrows', BorrowViewSet, basename='borrow-flat')  # Ensure this is set
router.register(r'reviews', ReviewViewSet, basename='review-flat')  # Ensure this is set

# Nested router for /books/{book_pk}/availablebooks/
books_router = routers.NestedDefaultRouter(router, r'books', lookup='book')
books_router.register(r'availablebooks', AvailableBookViewSet, basename='availablebook')

# Nested router for /books/{book_pk}/availablebooks/{availablebook_pk}/borrows/
availablebooks_router = routers.NestedDefaultRouter(books_router, r'availablebooks', lookup='availablebook')
availablebooks_router.register(r'borrows', BorrowViewSet, basename='borrow')

# Nested router for /books/{book_pk}/reviews/
books_router.register(r'reviews', ReviewViewSet, basename='review')

# URLs for registration and logout
router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),  # Flat routes should be included first
    path('', include(books_router.urls)),
    path('', include(availablebooks_router.urls)),
    path('auth/users', RegisterView.as_view()),
    path('auth/sessions', obtain_auth_token),
    path('auth/logout', LogoutView.as_view()),
]

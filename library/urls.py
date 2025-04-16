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


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet, basename='book')
router.register(r'available-books', AvailableBookViewSet, basename='available-book-flat')
router.register(r'borrows', BorrowViewSet, basename='borrow-flat')
router.register(r'reviews', ReviewViewSet, basename='review-flat')


books_router = routers.NestedDefaultRouter(router, r'books', lookup='book')
books_router.register(r'available-books', AvailableBookViewSet, basename='available-book')


availablebooks_router = routers.NestedDefaultRouter(books_router, r'available-books', lookup='availablebook')
availablebooks_router.register(r'borrows', BorrowViewSet, basename='borrow')


books_router.register(r'reviews', ReviewViewSet, basename='review')


router.register(r'users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('', include(books_router.urls)),
    path('', include(availablebooks_router.urls)),
    path('auth/users', RegisterView.as_view()),
    path('auth/sessions', obtain_auth_token),
    path('auth/logout', LogoutView.as_view()),
]

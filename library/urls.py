from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RegisterView, LogoutView, AvailableBookViewSet, BorrowViewSet, ReviewViewSet
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static

# Create a router and register our viewsets
router = DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet)  # Registers the 'books' endpoint with the viewset
router.register(r'availablebooks', AvailableBookViewSet)
router.register(r'borrows', BorrowViewSet)  # Registers the 'borrows' endpoint with the BorrowViewSet
router.register(r'reviews', ReviewViewSet)
# Define URL patterns (No trailing slashes here)
urlpatterns = [
    path('auth/users', RegisterView.as_view()),   # User registration
    path('auth/sessions', obtain_auth_token),     # User login (obtain auth token)
    path('auth/logout', LogoutView.as_view()),    # User logout
    path('', include(router.urls)),               # Include all the routes for books
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
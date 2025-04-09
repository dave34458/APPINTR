from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RegisterView, LogoutView
from rest_framework.authtoken.views import obtain_auth_token

# Create a router and register our viewsets
router = DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet)  # Registers the 'books' endpoint with the viewset

# Define URL patterns (No trailing slashes here)
urlpatterns = [
    path('auth/users', RegisterView.as_view()),   # User registration
    path('auth/sessions', obtain_auth_token),     # User login (obtain auth token)
    path('auth/logout', LogoutView.as_view()),    # User logout
    path('', include(router.urls)),               # Include all the routes for books
]

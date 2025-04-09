from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, RegisterView, LogoutView, AvailableBookViewSet, BorrowViewSet, ReviewViewSet
from rest_framework.authtoken.views import obtain_auth_token
from django.conf import settings
from django.conf.urls.static import static
router = DefaultRouter(trailing_slash=False)
router.register(r'books', BookViewSet)
router.register(r'availablebooks', AvailableBookViewSet)
router.register(r'borrows', BorrowViewSet)
router.register(r'reviews', ReviewViewSet)
urlpatterns = [
    path('auth/users', RegisterView.as_view()),
    path('auth/sessions', obtain_auth_token),
    path('auth/logout', LogoutView.as_view()),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
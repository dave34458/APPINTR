from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Book, Borrow, AvailableBook, Review
from .serializers import BookSerializer, BorrowSerializer, UserRegisterSerializer, ReviewSerializer, AvailableBookSerializer
from rest_framework.authtoken.models import Token

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], url_path='availablebooks')
    def available_books(self, request, pk=None):
        book = self.get_object()
        available_books = AvailableBook.objects.filter(book=book)
        serializer = AvailableBookSerializer(available_books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='availablebooks/(?P<available_book_id>\d+)/borrows')
    def available_book_borrows(self, request, pk=None, available_book_id=None):
        borrows = Borrow.objects.filter(available_book_id=available_book_id)
        serializer = BorrowSerializer(borrows, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='reviews')
    def reviews(self, request, pk=None):
        """List all reviews for a specific book."""
        book = self.get_object()
        reviews = Review.objects.filter(book=book)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class AvailableBookViewSet(viewsets.ModelViewSet):
    queryset = AvailableBook.objects.all()
    serializer_class = AvailableBookSerializer
    permission_classes = [IsAuthenticated]


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
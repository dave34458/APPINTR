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

    def get_available_copies(self, book):
        """Helper function to calculate available copies dynamically."""
        available_books = AvailableBook.objects.filter(book=book)
        available_count = 0

        for available_book in available_books:
            if available_book.is_available():
                available_count += 1

        return available_count

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Check book availability."""
        book = self.get_object()
        available_copies = self.get_available_copies(book)
        status = 'available' if available_copies > 0 else 'unavailable'
        return Response({'title': book.title, 'available_copies': available_copies, 'status': status})

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

class AvailableBookViewSet(viewsets.ModelViewSet):
    queryset = AvailableBook.objects.all()
    serializer_class = AvailableBookSerializer
    permission_classes = [IsAuthenticated]

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()  # Return all borrow records
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
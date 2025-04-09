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

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        """Allow staff to borrow a book from the available books list."""
        if not request.user.is_staff:
            return Response({"error": "Only staff can borrow books."}, status=status.HTTP_403_FORBIDDEN)

        available_book_id = request.data.get('available_book_id')
        if not available_book_id:
            return Response({"error": "available_book_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the AvailableBook and check if it's available.
        available_book = AvailableBook.objects.filter(id=available_book_id, book_id=pk).first()
        if not available_book or available_book.is_available() == False:
            return Response({"error": "No available copies."}, status=status.HTTP_400_BAD_REQUEST)

        # Create a borrow record.
        borrow = Borrow.objects.create(user=request.user, available_book=available_book)
        return Response(BorrowSerializer(borrow).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Allow user to review a book."""
        book = self.get_object()
        rating = request.data.get('rating', 0)  # default to 0 if not provided
        comment = request.data.get('comment', '')

        # Review model will automatically handle validation for rating.
        review = Review.objects.create(user=request.user, book=book, rating=rating, comment=comment)
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)

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
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter borrow records by the logged-in user."""
        user = self.request.user
        return Borrow.objects.filter(user=user)  # Optionally filter by the user
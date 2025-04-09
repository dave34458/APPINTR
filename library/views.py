from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Book, Borrow, AvailableBook, Review
from .serializers import BookSerializer, BorrowSerializer, UserRegisterSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token


# ViewSet for Book model
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Check book availability by calculating total copies and borrowed copies."""
        book = self.get_object()

        # Get the AvailableBook instances for the book
        available_books = AvailableBook.objects.filter(book=book)

        # Calculate the total number of available copies across all locations
        total_available_copies = sum(available_book.available_copies for available_book in available_books)

        # Calculate the number of borrowed copies for the book
        borrowed_copies = Borrow.objects.filter(book=book, return_date__isnull=True).count()

        # Calculate available copies (total copies - borrowed copies)
        available_copies = total_available_copies - borrowed_copies

        status = 'available' if available_copies > 0 else 'unavailable'

        return Response({
            'title': book.title,
            'available_copies': available_copies,
            'status': status
        })

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        """Allow user to borrow a book."""
        book = self.get_object()

        # Get the AvailableBook instances for the book
        available_books = AvailableBook.objects.filter(book=book)

        # Calculate the total number of available copies across all locations
        total_available_copies = sum(available_book.available_copies for available_book in available_books)

        # Calculate the number of borrowed copies for the book
        borrowed_copies = Borrow.objects.filter(book=book, return_date__isnull=True).count()

        # Calculate available copies (total copies - borrowed copies)
        available_copies = total_available_copies - borrowed_copies

        if available_copies <= 0:
            return Response({"error": "No available copies"}, status=status.HTTP_400_BAD_REQUEST)

        # Find the first available copy and update the stock
        available_book = available_books.first()  # This assumes there is at least one available location
        if available_book.available_copies > 0:
            available_book.available_copies -= 1
            available_book.save()
            borrow = Borrow.objects.create(user=request.user,
                                           book=book)  # Associate the borrow with the book, not available_book
            return Response(BorrowSerializer(borrow).data, status=status.HTTP_201_CREATED)

        return Response({"error": "No available copies"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Allow user to review a book."""
        book = self.get_object()
        rating = request.data.get('rating')
        comment = request.data.get('comment')

        # Ensure valid rating
        if not 1 <= int(rating) <= 5:
            return Response({"error": "Invalid rating"}, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(user=request.user, book=book, rating=rating, comment=comment)
        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


# User Registration
class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

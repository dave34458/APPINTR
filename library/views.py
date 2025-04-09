from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from .models import Book, Borrow, AvailableBook, Review
from .serializers import BookSerializer, BorrowSerializer, UserRegisterSerializer, ReviewSerializer
from rest_framework.authtoken.models import Token


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_available_copies(self, book):
        """Helper function to calculate available copies."""
        total_available = sum(available.available_copies for available in AvailableBook.objects.filter(book=book))
        borrowed = Borrow.objects.filter(book=book, return_date__isnull=True).count()
        return total_available - borrowed

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Check book availability."""
        book = self.get_object()
        available_copies = self.get_available_copies(book)
        status = 'available' if available_copies > 0 else 'unavailable'
        return Response({'title': book.title, 'available_copies': available_copies, 'status': status})

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        """Allow user to borrow a book."""
        book = self.get_object()
        available_copies = self.get_available_copies(book)

        if available_copies <= 0:
            return Response({"error": "No available copies"}, status=status.HTTP_400_BAD_REQUEST)

        available_book = AvailableBook.objects.filter(book=book).first()
        if available_book.available_copies > 0:
            available_book.available_copies -= 1
            available_book.save()
            borrow = Borrow.objects.create(user=request.user, book=book)
            return Response(BorrowSerializer(borrow).data, status=status.HTTP_201_CREATED)

        return Response({"error": "No available copies"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def review(self, request, pk=None):
        """Allow user to review a book."""
        book = self.get_object()
        rating = request.data.get('rating')
        comment = request.data.get('comment')

        if not (1 <= int(rating) <= 5):
            return Response({"error": "Invalid rating"}, status=status.HTTP_400_BAD_REQUEST)

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

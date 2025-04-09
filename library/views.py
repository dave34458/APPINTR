# library/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.views import obtain_auth_token
from .models import Book, Borrow
from .serializers import BookSerializer, BorrowSerializer, UserRegisterSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token


# ViewSet for Book model
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Check book availability."""
        book = self.get_object()
        borrowed_count = Borrow.objects.filter(book=book, return_date__isnull=True).count()
        available_copies = book.total_copies - borrowed_count
        status = 'available' if available_copies > 0 else 'unavailable'
        return Response({'title': book.title, 'available_copies': available_copies, 'status': status})

    @action(detail=True, methods=['post'])
    def borrow(self, request, pk=None):
        """Allow user to borrow a book."""
        book = self.get_object()
        borrowed_count = Borrow.objects.filter(book=book, return_date__isnull=True).count()

        if borrowed_count >= book.total_copies:
            return Response({"error": "No available copies"}, status=status.HTTP_400_BAD_REQUEST)

        borrow = Borrow.objects.create(user=request.user, book=book)
        return Response(BorrowSerializer(borrow).data, status=status.HTTP_201_CREATED)


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



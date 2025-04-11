from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .models import Book, Borrow, AvailableBook, Review
from .serializers import BookSerializer, BorrowSerializer, UserRegisterSerializer, ReviewSerializer, AvailableBookSerializer
from .permissions import IsStaffUser  # Import the custom permission class
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffUser]  # Allow GET for all, POST/PUT/DELETE for staff only


class AvailableBookViewSet(viewsets.ModelViewSet):
    queryset = AvailableBook.objects.all()  # Default queryset
    serializer_class = AvailableBookSerializer
    permission_classes = [IsStaffUser]  # Allow GET for all, POST/PUT/DELETE for staff only

    def get_queryset(self):
        queryset = super().get_queryset()
        book_pk = self.kwargs.get('book_pk')
        if book_pk:
            queryset = queryset.filter(book_id=book_pk)
        return queryset


class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    serializer_class = BorrowSerializer
    permission_classes = [IsStaffUser]  # Allow GET for all, POST/PUT/DELETE for staff only

    def get_queryset(self):
        queryset = super().get_queryset()
        borrow_id = self.kwargs.get('id')

        if borrow_id:
            queryset = queryset.filter(id=borrow_id)
        return queryset

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsStaffUser]

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

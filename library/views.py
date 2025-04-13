from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Book, Borrow, AvailableBook, Review, CustomUser
from .serializers import BookSerializer, BorrowReadSerializer, BorrowWriteSerializer, UserRegisterSerializer, ReviewSerializer, AvailableBookSerializer, CustomUserSerializer
from .permissions import IsStaffUser
from rest_framework.authtoken.models import Token

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffUser]

    @action(detail=True, methods=['get'], url_path='reviews')
    def get_reviews(self, request, pk=None):
        book = self.get_object()
        reviews = Review.objects.filter(book=book)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class AvailableBookViewSet(viewsets.ModelViewSet):
    queryset = AvailableBook.objects.all()
    serializer_class = AvailableBookSerializer
    permission_classes = [IsStaffUser]

    def get_queryset(self):
        queryset = super().get_queryset()
        if book_pk := self.kwargs.get('book_pk'):
            queryset = queryset.filter(book_id=book_pk)
        return queryset

class BorrowViewSet(viewsets.ModelViewSet):
    queryset = Borrow.objects.all()
    permission_classes = [IsStaffUser]

    def get_serializer_class(self):
        return BorrowReadSerializer if self.request.method == 'GET' else BorrowWriteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if book_id := self.kwargs.get('book_pk'):
            queryset = queryset.filter(available_book__book_id=book_id)
        if available_book_id := self.kwargs.get('available_book_pk'):
            queryset = queryset.filter(available_book_id=available_book_id)
        return queryset

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsStaffUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsStaffUser]

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'me':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, *args, **kwargs)

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

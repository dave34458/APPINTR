from rest_framework import viewsets, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Book, AvailableBook, Borrow, Review, CustomUser
from .serializers import BookSerializer, AvailableBookReadSerializer, AvailableBookWriteSerializer, ReviewSerializer, \
    BorrowReadSerializer, BorrowWriteSerializer, UserRegisterSerializer, CustomUserSerializer
from .permissions import IsStaffOrReadOnly, IsStaffOrReadOnlyExceptReviewPost

from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsStaffOrReadOnly]



class AvailableBookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        book_pk = self.kwargs.get('book_pk')
        if book_pk:
            return AvailableBook.objects.filter(book_id=book_pk)
        return AvailableBook.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AvailableBookReadSerializer  # Read serializer (with `copy_is_available`)
        return AvailableBookWriteSerializer  # Write serializer (with `book_id`)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy'] and not self.kwargs.get('book_pk'):
            self.permission_classes = []
        return super().get_permissions()


class BorrowViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        book_pk = self.kwargs.get('book_pk')
        availablebook_pk = self.kwargs.get('availablebook_pk')

        if book_pk and availablebook_pk:
            return Borrow.objects.filter(available_book__book_id=book_pk, available_book_id=availablebook_pk)
        if availablebook_pk:
            return Borrow.objects.filter(available_book_id=availablebook_pk)
        return Borrow.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BorrowReadSerializer
        return BorrowWriteSerializer

    def get_permissions(self):
        # If on the flat URI and trying to do a non-GET action (POST, PUT, DELETE, etc.), raise a PermissionDenied
        if self.action not in ['list', 'retrieve'] and not self.kwargs.get('book_pk'):
            raise PermissionDenied("You are not allowed to perform this action on the flat URI.")
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = [IsStaffOrReadOnlyExceptReviewPost]

    def get_queryset(self):
        book_pk = self.kwargs.get('book_pk')
        if book_pk:
            return Review.objects.filter(book_id=book_pk)
        return Review.objects.all()

    def perform_create(self, serializer):
        book_pk = self.kwargs.get('book_pk')
        if book_pk:
            serializer.save(book_id=book_pk, user=self.request.user)
        else:
            serializer.save(user=self.request.user)

    def get_permissions(self):
        # If on the flat URI and trying to do a non-GET action (POST, PUT, DELETE, etc.), raise a PermissionDenied
        if self.action not in ['list', 'retrieve'] and not self.kwargs.get('book_pk'):
            raise PermissionDenied("You are not allowed to perform this action on the flat URI.")
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReviewSerializer
        return ReviewSerializer


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

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        if kwargs.get('pk') == 'me':
            return Response(self.get_serializer(request.user).data)
        return super().retrieve(request, *args, **kwargs)
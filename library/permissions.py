from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Allow anyone to read.
    Only staff can write (POST/PUT/PATCH/DELETE).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == 'staff'

class IsStaffOrReadOnlyExceptReviewPost(permissions.BasePermission):
    """
    Allow anyone to read.
    Allow any authenticated user to POST.
    Only staff can PUT/PATCH/DELETE.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.role == 'staff'

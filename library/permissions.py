from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffUser(BasePermission):
    """
    Custom permission class to restrict access to staff users.
    - GET: Allowed for everyone except UserViewSet
    - POST/PUT/PATCH/DELETE: Only allowed for staff users
    """

    def has_permission(self, request, view):
        # Allow GET/HEAD/OPTIONS for everyone except UserViewSet
        if request.method in SAFE_METHODS and view.basename != 'user':
            return True

        # POST for reviews: Authenticated users can post reviews
        if request.method == 'POST' and view.basename == 'review':
            return request.user.is_authenticated

        # For POST/PUT/PATCH/DELETE: Only staff can modify resources
        return request.user.is_authenticated and request.user.role == 'staff'

    def has_object_permission(self, request, view, obj):
        # Allow GET/HEAD/OPTIONS for everyone except UserViewSet
        if request.method in SAFE_METHODS and view.basename != 'user':
            return True

        # POST for reviews: Authenticated users can post reviews
        if request.method == 'POST' and view.basename == 'review':
            return request.user.is_authenticated

        # PUT/PATCH/DELETE: Only staff can modify resources
        return request.user.is_authenticated and request.user.role == 'staff'

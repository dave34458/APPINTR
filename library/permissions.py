from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffUser(BasePermission):
    """
    - GET: available to everyone
    - POST: only for logged-in users (but only for reviews)
    - PUT/PATCH/DELETE: only for staff users
    """

    def has_permission(self, request, view):
        # Allow GET/HEAD/OPTIONS for everyone (including non-authenticated users)
        if request.method in SAFE_METHODS:
            return True

        # POST:
        if request.method == 'POST':
            # Authenticated users (not staff) can post reviews
            if request.user.is_authenticated and view.basename == 'review':
                return True
            # Staff can post anything
            return request.user.is_authenticated and request.user.role == 'staff'

        # For PUT/PATCH/DELETE: only staff can modify resources
        return request.user.is_authenticated and request.user.role == 'staff'

    def has_object_permission(self, request, view, obj):
        # Allow GET/HEAD/OPTIONS for everyone
        if request.method in SAFE_METHODS:
            return True

        # PUT/PATCH/DELETE: only staff can modify resources
        return request.user.is_authenticated and request.user.role == 'staff'

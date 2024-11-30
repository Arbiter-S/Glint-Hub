from rest_framework.permissions import BasePermission


class VerificationPermission(BasePermission):

    def has_permission(self, request, view):
            user = request.user
            user_id = user.id
            requested_user_id = view.kwargs.get('user_id')
            if user_id == requested_user_id:
                return True
            return False

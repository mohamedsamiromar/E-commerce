from rest_framework.permissions import BasePermission


class IsMerchant(BasePermission):
    message = 'You must be an approved merchant to access this resource.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'merchant_profile')
            and request.user.merchant_profile.is_approved
        )

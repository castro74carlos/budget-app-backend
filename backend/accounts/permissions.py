from rest_framework import permissions

from .models import Account


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to allow access only to the owner of an object or its parent object.
    """

    def has_permission(self, request, view):
        if (view.action == 'create' or view.action == 'update') and not request.user.is_staff and not request.user.is_superuser:

            account_url = request.data.get('account')
            account_owner = request.data.get('account_owner')
            if account_owner:
                return int(account_owner) == int(request.user.id)
            elif not account_url:
                return True
            else:
                # Extract the ID from the URL
                account_id = account_url.rstrip('/').split('/')[-1]

                try:
                    account = Account.objects.get(id=account_id)
                    return account.account_owner == request.user
                except Account.DoesNotExist:
                    return False

        return True

    def has_object_permission(self, request, view, obj):
        # Allow access for admin users
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Check ownership of the parent object (e.g., Project)
        if hasattr(obj, 'account') and obj.account.account_owner == request.user:
            print(obj.account.account_owner)
            return True
        # Check ownership directly on the object
        if hasattr(obj, 'account_owner') and obj.account_owner == request.user:
            return True
        return False
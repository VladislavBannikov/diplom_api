from rest_framework import permissions


class OrderPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'partial_update']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated:
            return False
        if view.action == 'partial_update':
            return obj.user_id == request.user.id
        else:
            return False


class OnlyBuyers(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.type == 'buyer':
            return True
        else:
            return False


class OnlyShops(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.type == 'shop':
            return True
        else:
            return False

from rest_framework import permissions


class IsRestaurantOwner(permissions.BasePermission):
    """
    Custom permission to only allow restaurant owners to access their own data.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'restaurant'
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the restaurant
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'restaurant'):
            return obj.restaurant.user == request.user
        return False


class IsProviderOwner(permissions.BasePermission):
    """
    Custom permission to only allow provider owners to access their own data.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'provider'
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the provider
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'provider'):
            return obj.provider.user == request.user
        return False

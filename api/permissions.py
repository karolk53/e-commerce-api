from rest_framework import permissions


class IsSeller(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_seller


class IsCustomer(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.is_customer
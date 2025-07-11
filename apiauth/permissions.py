from rest_framework import permissions


class IsHR(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_hr
    

class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
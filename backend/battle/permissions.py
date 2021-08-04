from rest_framework.permissions import BasePermission


class IsInBattle(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in [obj.creator, obj.opponent]


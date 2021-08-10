from rest_framework.permissions import BasePermission

from battle.models import Battle


class IsInBattle(BasePermission):

    message = "ERROR: You do not have permission for this action."

    def has_permission(self, request, view):
        if request.method == 'POST' and request.data.get('battle'):
            battle = Battle.objects.get(id=request.data['battle'])
            return request.data['trainer'] in (str(battle.creator.id), str(battle.opponent.id))
        return True

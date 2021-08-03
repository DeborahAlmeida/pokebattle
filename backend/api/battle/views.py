from django.db.models import Q
from battle.models import Battle
from api.battle.serializers import BattleSerializer
from rest_framework import generics, permissions


class BattletList(generics.ListCreateAPIView):

    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by('-id')
        return queryset

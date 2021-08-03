from django.db.models import Q
from rest_framework import generics, permissions
from battle.models import Battle
from api.battle.serializers import BattleSerializer


class BattletList(generics.ListCreateAPIView):

    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by('-id')
        return queryset


class BattleDetail(generics.RetrieveAPIView):
    serializer_class = BattleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by('-id')
        return queryset

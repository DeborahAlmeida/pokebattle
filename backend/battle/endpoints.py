from django.db.models import Q

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from battle.permissions import IsInBattle
from battle.models import Battle
from battle.serializers import (
    BattleSerializer,
    BattleCreateSerializer,
    TeamCreateSerializer,
    UserSerializer
)


class BattletList(generics.ListCreateAPIView):
    serializer_class = BattleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by('-id')
        return queryset


class BattleDetail(generics.RetrieveAPIView):
    serializer_class = BattleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Battle.objects.filter(
            Q(creator=self.request.user) | Q(opponent=self.request.user)
        ).order_by('-id')
        return queryset


class BattleCreate(generics.CreateAPIView):
    serializer_class = BattleCreateSerializer
    permission_classes = [IsAuthenticated]


class TeamCreate(generics.CreateAPIView):
    serializer_class = TeamCreateSerializer
    permission_classes = [IsInBattle]


class CurrentUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(
            request.user,
            context={'request': request}
        )
        return Response(serializer.data)

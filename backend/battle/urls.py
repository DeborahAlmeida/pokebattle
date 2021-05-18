from django.urls import path
from .views import (
    Home,
    BattleView,
    Invite,
    TeamView,
)


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("battle/", BattleView.as_view(), name="battle"),
    path('invite/', Invite.as_view(), name='invite'),
    path("team/<int:pk>/create", TeamView.as_view(), name="team_create"),
]

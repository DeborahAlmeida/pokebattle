from django.urls import path
from .views import (
    Home,
    BattleView,
    Invite,
    TeamView,
    BattleList,
    BattleDetail,
)


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("battle/", BattleView.as_view(), name="battle"),
    path('invite/', Invite.as_view(), name='invite'),
    path('battle/list', BattleList.as_view(), name='battle_list'),
    path("team/<int:pk>/create/<int:user>", TeamView.as_view(), name="team_create"),
    path("battle/detail/<int:pk>", BattleDetail.as_view(), name="battle_detail"),

]

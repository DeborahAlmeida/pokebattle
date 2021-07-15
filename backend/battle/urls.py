from django.urls import path
from .views import (
    Home,
    BattleView,
    Invite,
    TeamView,
    BattleList,
    BattleDetail,
    BattleSignUp,
    SignUpSucess,
    PasswordCreateConfirmView,
    PasswordCreateCompleteView,
)
from django.urls import reverse_lazy

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("battle/", BattleView.as_view(), name="battle"),
    path('invite/', Invite.as_view(), name='invite'),
    path('battle/list/', BattleList.as_view(), name='battle_list'),
    path("team/<int:pk>/create/", TeamView.as_view(), name="team_create"),
    path("battle/detail/<int:pk>/", BattleDetail.as_view(), name="battle_detail"),
    path('signup/', BattleSignUp.as_view(), name='signup'),
    path('signup/sucess', SignUpSucess.as_view(), name='signup_sucess'),
    path(
        'create/<uidb64>/<token>/',
        PasswordCreateConfirmView.as_view(
            success_url=reverse_lazy(
                'password_create_complete')), name='password_create_confirm'),
    path(
        'create/done/',
        PasswordCreateCompleteView.as_view(),
        name='password_create_complete'),

]

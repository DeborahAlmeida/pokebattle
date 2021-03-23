from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('battle/new/', views.battle_new, name='battle_new'),
    path('round/new/', views.round_new, name='round_new'),
    path('invite/', views.invite, name='invite'),
    path('player2/', views.player2, name='player2'),
    path('player2/round', views.round_new2, name='round_new2'),

]
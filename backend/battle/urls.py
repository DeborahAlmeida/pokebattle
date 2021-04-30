from django.urls import path
from . import views
from .views import (
    Home,
    #RoundNewCreator,
    #RoundNewOponnent,
    #Invite,
    #Opponent, 
)

urlpatterns = [
    path("", Home.as_view(), name="home"),
    #path('round/new/', RoundNewCreator.as_view(), name='round_new'),
    #path('invite/', Invite.as_view(), name='invite'),
    #path('opponent/', Opponent.as_view(), name='opponent'),
    #path('player2/round', RoundNewOponnent.as_view() , name='round_new2'),

]

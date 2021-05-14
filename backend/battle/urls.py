from django.urls import path
from .views import (
    Home,
    BattleView,
    Invite,
    PokemonTeamView,
    # RoundNewCreator,
    # RoundNewOponnent,
    # Invite,
    # Opponent,
)


urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("battle/", BattleView.as_view(), name="battle"),
    path("battle/pokemon", PokemonTeamView.as_view(), name="pokemon_team"),
    # path('round/new/', RoundNewCreator.as_view(), name='round_new'),
    path('invite/', Invite.as_view(), name='invite'),
    # path('opponent/', Opponent.as_view(), name='opponent'),
    # path('player2/round', RoundNewOponnent.as_view() , name='round_new2'),

]

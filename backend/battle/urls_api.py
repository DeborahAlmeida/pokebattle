from django.urls import path
from battle import endpoints

urlpatterns = [
    path('battles/', endpoints.BattlesList.as_view(), name="api_battle_list"),
    path("battle/<int:pk>/", endpoints.BattleDetail.as_view(), name="api_battle_detail"),
    path("battle/create/", endpoints.BattleCreate.as_view(), name="api_battle_create"),
    path("team/create/", endpoints.TeamCreate.as_view(), name="api_team_create"),
    path("user/", endpoints.CurrentUser.as_view(), name="api_current_user"),
    path('pokemons/', endpoints.PokemonsList.as_view(), name="api_pokemon_list"),
]

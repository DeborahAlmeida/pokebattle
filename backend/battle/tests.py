
from django.test import TestCase, Client
from battle.battles.battle import validate_sum_pokemons
from model_bakery import baker
from battle.models import PokemonTeam
from battle.battles.battle import get_winner_for


class GetWinnerTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.creator, self.opponent = baker.make('users.User', _quantity=2)
        self.pokemon_1, self.pokemon_2, self.pokemon_3 = baker.make(
            "pokemon.Pokemon",
            attack=60, defense=45, hp=50, _quantity=3)
        self.battle = baker.make('battle.Battle', creator=self.creator, opponent=self.opponent)
        self.team_creator = baker.make('battle.Team', battle=self.battle, trainer=self.creator)
        self.team_opponent = baker.make('battle.Team', battle=self.battle, trainer=self.opponent)
        PokemonTeam.objects.create(team=self.team_creator, pokemon=self.pokemon_1, order=1)
        PokemonTeam.objects.create(team=self.team_creator, pokemon=self.pokemon_2, order=2)
        PokemonTeam.objects.create(team=self.team_creator, pokemon=self.pokemon_3, order=3)
        PokemonTeam.objects.create(team=self.team_opponent, pokemon=self.pokemon_1, order=1)
        PokemonTeam.objects.create(team=self.team_opponent, pokemon=self.pokemon_2, order=2)
        PokemonTeam.objects.create(team=self.team_opponent, pokemon=self.pokemon_3, order=3)

    def test_verify_if_returns_correct_winner(self):
        winner = get_winner_for(self.team_creator, self.team_opponent)
        self.assertEqual(winner, self.team_creator)

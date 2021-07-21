from django.test import TestCase, Client
from model_bakery import baker
from battle.models import PokemonTeam
from battle.battles.battle import get_winner_for


class GetWinnerTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.creator, self.opponent = baker.make('users.User', _quantity=2)
        self.battle = baker.make('battle.Battle', creator=self.creator, opponent=self.opponent)
        self.team_creator = baker.make('battle.Team', battle=self.battle, trainer=self.creator)
        self.team_opponent = baker.make('battle.Team', battle=self.battle, trainer=self.opponent)
        self.pokemon_1, self.pokemon_2, self.pokemon_3 = baker.make(
            "pokemon.Pokemon",
            attack=60, defense=45, hp=50, _quantity=3)

    def test_verify_if_returns_creator_as_winner_when_draw(self):
        pokemons = [self.pokemon_1, self.pokemon_2, self.pokemon_3]
        count_creator = 0
        count_opponent = 0
        while count_creator < 3:
            PokemonTeam.objects.create(
                team=self.team_creator,
                pokemon=pokemons[count_creator],
                order=count_creator)
            count_creator = count_creator + 1
        
        while count_opponent < 3:
            PokemonTeam.objects.create(
                team=self.team_opponent,
                pokemon=pokemons[count_opponent],
                order=count_opponent)
            count_opponent = count_opponent + 1

        winner = get_winner_for(self.team_creator, self.team_opponent)
        self.assertEqual(winner, self.team_creator)

    def test_verify_if_returns_winner_when_different_points(self):
        pokemon_4, pokemon_5, pokemon_6 = baker.make(
            "pokemon.Pokemon",
            attack=100, defense=35, hp=30, _quantity=3)
        pokemons_creator = [self.pokemon_1, self.pokemon_2, self.pokemon_3]
        pokemons_opponent = [pokemon_4, pokemon_5, pokemon_6]
        count_creator = 0
        count_opponent = 0
        while count_creator < 3:
            PokemonTeam.objects.create(
                team=self.team_creator,
                pokemon=pokemons_creator[count_creator],
                order=count_creator)
            count_creator = count_creator + 1

        while count_opponent < 3:
            PokemonTeam.objects.create(
                team=self.team_opponent,
                pokemon=pokemons_opponent[count_opponent],
                order=count_opponent)
            count_opponent = count_opponent + 1

        winner = get_winner_for(self.team_creator, self.team_opponent)
        self.assertEqual(winner, self.team_creator)

    def test_verify_if_not_returns_winner_missing_pokemons_teams(self):
        pokemon_4, pokemon_5, pokemon_6 = baker.make(
            "pokemon.Pokemon",
            attack=100, defense=35, hp=30, _quantity=3)
        pokemons_creator = [self.pokemon_1, self.pokemon_2, self.pokemon_3]
        pokemons_opponent = [pokemon_4, pokemon_5, pokemon_6]
        count_creator = 0
        count_opponent = 0
        while count_creator < 3:
            PokemonTeam.objects.create(
                team=self.team_creator,
                pokemon=pokemons_creator[count_creator],
                order=count_creator)
            count_creator = count_creator + 1
   
        while count_opponent < 2:
            PokemonTeam.objects.create(
                team=self.team_opponent,
                pokemon=pokemons_opponent[count_opponent],
                order=count_opponent)
            count_opponent = count_opponent + 1
        try:
            get_winner_for(self.team_creator, self.team_opponent)
        except IndexError:
            pass

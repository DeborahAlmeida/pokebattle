from django.core.exceptions import ValidationError
from django.test import TestCase, Client
from model_bakery import baker
from django.urls import reverse
from battle.models import PokemonTeam, Team
from battle.battles.battle import get_winner_for
from users.models import User


class GetWinnerTest(TestCase):
    def setUp(self):
        super().setUp()
        self.creator, self.opponent = baker.make('users.User', _quantity=2)
        battle = baker.make('battle.Battle', creator=self.creator, opponent=self.opponent)
        self.team_creator = baker.make('battle.Team', battle=battle, trainer=self.creator)
        self.team_opponent = baker.make('battle.Team', battle=battle, trainer=self.opponent)
        self.pokemon_1, self.pokemon_2, self.pokemon_3 = baker.make(
            "pokemon.Pokemon",
            attack=60, defense=45, hp=50, _quantity=3)

    def test_verify_if_returns_creator_as_winner_when_draw(self):
        pokemons = [self.pokemon_1, self.pokemon_2, self.pokemon_3]
        for count, pokemon in enumerate(pokemons):
            PokemonTeam.objects.create(
                team=self.team_creator,
                pokemon=pokemon,
                order=count)

        for count, pokemon in enumerate(pokemons):
            PokemonTeam.objects.create(
                team=self.team_opponent,
                pokemon=pokemon,
                order=count)

        winner = get_winner_for(self.team_creator, self.team_opponent)
        self.assertEqual(winner, self.team_creator)

    def test_verify_if_returns_winner_when_different_points(self):
        pokemon_4, pokemon_5, pokemon_6 = baker.make(
            "pokemon.Pokemon",
            attack=100, defense=35, hp=30, _quantity=3)
        pokemons_creator = [self.pokemon_1, self.pokemon_2, self.pokemon_3]
        pokemons_opponent = [pokemon_4, pokemon_5, pokemon_6]
        for count, pokemon in enumerate(pokemons_creator):
            PokemonTeam.objects.create(
                team=self.team_creator,
                pokemon=pokemon,
                order=count)

        for count, pokemon in enumerate(pokemons_opponent):
            PokemonTeam.objects.create(
                team=self.team_opponent,
                pokemon=pokemon,
                order=count)

        winner = get_winner_for(self.team_creator, self.team_opponent)
        self.assertEqual(winner, self.team_creator)

    def test_verify_if_not_returns_winner_missing_pokemons_teams(self):
        pokemon_4, pokemon_5 = baker.make(
            "pokemon.Pokemon",
            attack=100, defense=35, hp=30, _quantity=2)
        pokemons_creator = [self.pokemon_1, self.pokemon_2, self.pokemon_3]
        pokemons_opponent = [pokemon_4, pokemon_5]

        for count, pokemon in enumerate(pokemons_creator):
            PokemonTeam.objects.create(
                team=self.team_creator,
                pokemon=pokemon,
                order=count)

        for count, pokemon in enumerate(pokemons_opponent):
            PokemonTeam.objects.create(
                team=self.team_opponent,
                pokemon=pokemon,
                order=count)

        with self.assertRaises(IndexError):
            get_winner_for(self.team_creator, self.team_opponent)


class AssociatePokemonsToBattleTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.user = User.objects.create(email='example@example.com')
        self.user.set_password('admin')
        self.user.save()
        self.battle = baker.make('battle.Battle', creator=self.user)
        names = ['pikachu', 'bulbasaur', 'pidgeot', 'wrong_name']
        for pokemon_name in names:
            baker.make("pokemon.Pokemon", name=pokemon_name, attack=60, defense=15, hp=10)

    def test_user_can_create_team_with_pokemons(self):
        self.client.login(username=self.user.email, password='admin')
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        response = self.client.post(
            reverse("team_create", kwargs={'pk': self.battle.id}), pokemons_data, follow=True)
        self.assertEqual(response.status_code, 200)
        team_user = Team.objects.filter(trainer=self.user)
        self.assertTrue(team_user)

    def test_if_returns_error_when_type_wrong_pokemon_name(self):
        self.client.login(username=self.user.email, password='admin')
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user.id,
            "pokemon_1": 'wrong_name',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        response = self.client.post(reverse("team_create", kwargs={'pk': self.battle.id}), pokemons_data, follow=True)
        self.assertEqual(response.context_data['form'].errors['__all__'][0], 'ERROR: Type the correct pokemons name')

    def test_if_returns_error_when_missing_position(self):
        self.client.login(username=self.user.email, password='admin')
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
        }
        with self.assertRaises(KeyError):
            self.client.post(reverse(
                "team_create", kwargs={'pk': self.battle.id}), pokemons_data, follow=True)

    def test_if_returns_error_when_user_is_not_permited(self):
        self.client.login(username=self.user.email, password='admin')
        user_not_permited = baker.make('users.User')
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": user_not_permited.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        response = self.client.post(
            reverse(
                "team_create",
                kwargs={'pk': self.battle.id}), pokemons_data, follow=True)
        self.assertEqual(
            response.context_data['form'].errors['__all__'][0],
            'ERROR: You do not have permission for this action.')

    def test_if_returns_error_when_missing_pokemons(self):
        self.client.login(username=self.user.email, password='admin')
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user.id,
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        response = self.client.post(
            reverse(
                "team_create",
                kwargs={'pk': self.battle.id}), pokemons_data, follow=True)
        self.assertEqual(
            response.context_data['form'].errors['__all__'][0],
            'ERROR: Select all pokemons')

    def test_if_returns_error_when_battle_does_not_exist(self):
        self.client.login(username=self.user.email, password='admin')
        pokemons_data = {
            "battle": 100,
            "trainer": self.user.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        with self.assertRaises(KeyError):
            self.client.post(reverse(
                "team_create", kwargs={'pk': 100}), pokemons_data, follow=True)


from model_bakery import baker
from common.utils.tests import TestCaseUtils
from django.urls import reverse
from battle.models import PokemonTeam, Team


class TeamViewTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.battle = baker.make('battle.Battle', creator=self.user)
        names = ['pikachu', 'bulbasaur', 'pidgeot', 'wrong_name']
        for pokemon_name in names:
            baker.make("pokemon.Pokemon", name=pokemon_name, attack=60, defense=15, hp=10)

    def test_user_can_create_team_with_pokemons(self):
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
        response = self.auth_client.post(
            reverse("team_create", kwargs={'pk': self.battle.id}), pokemons_data, follow=True)
        self.assertEqual(response.status_code, 200)

        team_user = Team.objects.get(battle=self.battle, trainer=self.user)
        self.assertTrue(team_user)

        pokemons_on_team_user = []

        pokemons_data_submited = [
            pokemons_data['pokemon_1'],
            pokemons_data['pokemon_2'],
            pokemons_data['pokemon_3']
        ]

        all_pokemons_on_team = PokemonTeam.objects.filter(
            team=team_user).prefetch_related('pokemon')

        for count in enumerate(pokemons_data_submited):
            pokemons_on_team_user.append(all_pokemons_on_team[count[0]].pokemon.name)

        self.assertEqual(pokemons_on_team_user, pokemons_data_submited)
        self.assertEqual(
            set(pokemons_data_submited), 
            set([p.name for p in team_user.pokemons.all()])
        )

    def test_if_returns_error_when_type_wrong_pokemon_name(self):
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
        response = self.auth_client.post(
            reverse("team_create", kwargs={'pk': self.battle.id}),
            pokemons_data, follow=True)

        self.assertEqual(
            response.context_data['form'].errors['__all__'][0],
            'ERROR: Type the correct pokemons name')

    def test_if_returns_error_when_missing_position(self):
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
        }
        response = self.auth_client.post(reverse(
            "team_create", kwargs={'pk': self.battle.id}), pokemons_data, follow=True)

        self.assertEqual(
            response.context_data['form'].errors['__all__'][0],
            'ERROR: Select all positions')

    def test_if_returns_error_when_user_is_not_permited(self):
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
        response = self.auth_client.post(
            reverse(
                "team_create",
                kwargs={'pk': self.battle.id}), pokemons_data, follow=True)
        self.assertEqual(
            response.context_data['form'].errors['__all__'][0],
            'ERROR: You do not have permission for this action.')

    def test_if_returns_error_when_missing_pokemons(self):
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user.id,
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        response = self.auth_client.post(
            reverse(
                "team_create",
                kwargs={'pk': self.battle.id}), pokemons_data, follow=True)
        self.assertEqual(
            response.context_data['form'].errors['__all__'][0],
            'ERROR: Select all pokemons')

    def test_if_returns_error_when_battle_does_not_exist(self):
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
        response = self.auth_client.post(reverse(
            "team_create", kwargs={'pk': 100}), pokemons_data, follow=True)
        self.assertEqual(response.status_code, 404)

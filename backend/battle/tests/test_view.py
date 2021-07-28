from model_bakery import baker
from common.utils.tests import TestCaseUtils
from django.urls import reverse
from battle.models import Battle, PokemonTeam
from battle.battles.battle import get_winner_for


class ListBattlesTest(TestCaseUtils):

    def test_login_user_can_acess_battle_list(self):
        response = self.auth_client.get(reverse('battle_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_returns_empty_list(self):
        response = self.auth_client.get(reverse('battle_list'))
        response_qs = response.context_data.get('battle_list')
        self.assertCountEqual(response_qs, Battle.objects.filter(creator=self.user))

    def test_view_returns_one_battle_in_list(self):
        baker.make('battle.Battle', creator=self.user)
        response = self.auth_client.get(reverse('battle_list'))
        response_qs = response.context_data.get('battle_list')
        self.assertCountEqual(response_qs, [Battle.objects.get(creator=self.user)])

    def test_view_returns_few_battle_ids(self):
        baker.make('battle.Battle', creator=self.user, _quantity=3)
        baker.make('battle.Battle', creator=self.user, _quantity=4)
        response = self.auth_client.get(reverse('battle_list'))
        response_qs = response.context_data.get('battle_list')
        self.assertCountEqual(Battle.objects.filter(creator=self.user), response_qs)

    def test_view_returns_a_lot_battle_ids(self):
        baker.make('battle.Battle', creator=self.user, _quantity=100)
        response = self.auth_client.get(reverse('battle_list'))
        response_qs = response.context_data.get('battle_list')
        self.assertCountEqual(Battle.objects.filter(creator=self.user), response_qs)

    def test_view_returns_an_error_when_the_user_is_not_logged(self):
        self.auth_client.logout()
        response = self.client.get(reverse('battle_list'))
        self.assertRedirects(response, '/accounts/login/?next=/battle/list/')
        self.assertEqual(response.status_code, 302)

    def test_view_diff_to_verify_it_returns_exactly_len_of_battle_list(self):
        baker.make('battle.Battle', creator=self.user, _quantity=10)

        response_initial = self.auth_client.get(reverse('battle_list'))
        response_qs_initial = response_initial.context_data.get('battle_list')

        self.assertCountEqual(Battle.objects.filter(creator=self.user), response_qs_initial)

        baker.make('battle.Battle', creator=self.user, _quantity=90)

        response_updated = self.auth_client.get(reverse('battle_list'))
        response_qs_updated = response_updated.context_data.get('battle_list')

        self.assertCountEqual(Battle.objects.filter(creator=self.user), response_qs_updated)


class BattleCreateViewTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make('users.User')

    def test_create_battle_successfully(self):
        battle_data = {
            "creator": self.user.id,
            "opponent": self.opponent.email,
        }
        self.auth_client.post(reverse('battle'), battle_data)
        battle = Battle.objects.filter(creator=self.user, opponent=self.opponent)
        self.assertTrue(battle)

    def test_if_returns_error_when_creator_and_opponent_are_the_same_user(self):
        battle_data = {
            "creator": self.user.id,
            "opponent": self.user.email,
        }
        response = self.auth_client.post(reverse('battle'), battle_data)
        self.assertEqual(
            response.context_data['form'].errors['__all__'][0],
            "ERROR: You can't challenge yourself.")

    def test_if_returns_error_when_opponent_doesnt_exist(self):
        battle_data = {
            "creator": self.user.id,
        }
        response = self.auth_client.post(reverse('battle'), battle_data)
        self.assertEqual(
            response.context_data['form'].errors['__all__'][0],
            "ERROR: You need to choose an opponent")


class GetWinnerTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make('users.User')
        battle = baker.make('battle.Battle', creator=self.user, opponent=self.opponent)
        self.team_creator = baker.make('battle.Team', battle=battle, trainer=self.user)
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

from django.test import TestCase, Client
from django.conf import settings
from unittest.mock import patch
from model_bakery import baker
from django.urls import reverse
from users.models import User
from pokemon.helpers import get_pokemon_from_api

from battle.models import Battle, PokemonTeam
from battle.battles.battle import get_winner_for
from battle.tasks import run_battle_and_send_result_email


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


class ListBattlesTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.battle = baker.make('battle.Battle')
        self.user = User.objects.create(email='example@example.com')
        self.user.set_password('admin')
        self.user.save()

    def test_login_user_can_acess_battle_list(self):
        self.client.login(username=self.user.email, password='admin')
        response = self.client.get(reverse('battle_list'))
        self.assertEqual(response.status_code, 200)

    def test_data_returns_empty_list(self):
        self.client.login(username=self.user.email, password='admin')
        response = self.client.get(reverse('battle_list'))
        response_qs = response.context_data.get('battle_list')
        self.assertCountEqual(response_qs, [])

    def test_data_returns_one_battle_in_list(self):
        self.client.login(username=self.user.email, password='admin')
        battle = baker.make('battle.Battle', creator=self.user)
        response = self.client.get(reverse('battle_list'))
        response_qs = response.context_data.get('battle_list')
        self.assertCountEqual(response_qs, [battle])

    def test_data_returns_few_battle_ids(self):
        self.client.login(username=self.user.email, password='admin')
        battles = baker.make('battle.Battle', creator=self.user, _quantity=4)
        response = self.client.get(reverse('battle_list'))
        response_qs = response.context_data.get('battle_list')
        self.assertCountEqual(battles, response_qs)

    def test_data_returns_a_lot_battle_ids(self):
        self.client.login(username=self.user.email, password='admin')
        battles = baker.make('battle.Battle', creator=self.user, _quantity=100)
        response = self.client.get(reverse('battle_list'))
        response_qs = response.context_data.get('battle_list')
        self.assertCountEqual(battles, response_qs)

    def test_data_an_error_when_the_user_is_not_logged(self):
        response = self.client.get(reverse('battle_list'))
        self.assertEqual(response.status_code, 302)

    def test_data_diff_to_verify_it_returns_exactly_len_of_battle_list(self):
        self.client.login(username=self.user.email, password='admin')

        baker.make('battle.Battle', creator=self.user, _quantity=10)
        battles_initial = Battle.objects.filter(creator=self.user)
        response_initial = self.client.get(reverse('battle_list'))
        response_qs_initial = response_initial.context_data.get('battle_list')

        self.assertCountEqual(battles_initial, response_qs_initial)

        baker.make('battle.Battle', creator=self.user, _quantity=90)
        battles_updated = Battle.objects.filter(creator=self.user)
        response_updated = self.client.get(reverse('battle_list'))
        response_qs_updated = response_updated.context_data.get('battle_list')

        self.assertCountEqual(battles_updated, response_qs_updated)


class BattleCreateViewTest(TestCase):
    def setUp(self):
        super().setUp()
        self.client = Client()
        self.creator = User.objects.create(email='example@example.com')
        self.creator.set_password('admin')
        self.creator.save()
        self.opponent = baker.make('users.User')

    def test_create_battle_successfully(self):
        battle_data = {
            "creator": self.creator.id,
            "opponent": self.opponent.email,
        }
        self.client.login(username=self.creator.email, password='admin')
        self.client.post(reverse('battle'), battle_data)
        battle = Battle.objects.filter(creator=self.creator, opponent=self.opponent)
        self.assertTrue(battle)

    def test_if_returns_error_when_creator_and_opponent_are_the_same_user(self):
        battle_data = {
            "creator": self.creator.id,
            "opponent": self.creator.email,
        }
        self.client.login(username=self.creator.email, password='admin')
        response = self.client.post(reverse('battle'), battle_data)
        self.assertEqual(
            response.context_data['form'].errors['__all__'][0],
            "ERROR: You can't challenge yourself.")

    def test_if_returns_error_when_opponent_doesnt_exist(self):
        battle_data = {
            "creator": self.creator.id,
            "opponent": 100,
        }
        self.client.login(username=self.creator.email, password='admin')
        with self.assertRaises(KeyError):
            self.client.post(reverse('battle'), battle_data)

    @patch("battle.battles.email.send_templated_mail")
    def test_if_battle_invitation_email_is_sent(self, mock_templated_mail):
        battle_data = {
            "creator": self.creator.id,
            "opponent": self.opponent.email,
        }

        self.client.login(username=self.creator.email, password='admin')

        self.client.post(reverse("battle"), battle_data)

        battle = Battle.objects.filter(
            creator=self.creator, opponent=self.opponent)

        self.assertTrue(battle)

        mock_templated_mail.assert_called_with(
            template_name="invite_challenge",
            from_email=settings.FROM_EMAIL,
            recipient_list=[self.opponent.email],
            context={
                'creator': self.creator.email,
            },
        )

    @patch('battle.tasks.run_battle')
    def test_if_run_battle_task(self, result_battle_mock):
        battle = Battle.objects.create(creator=self.creator, opponent=self.opponent)

        team_creator = baker.make('battle.Team', battle=battle, trainer=self.creator)
        team_opponent = baker.make('battle.Team', battle=battle, trainer=self.opponent)
        pokemon_1, pokemon_2, pokemon_3 = baker.make(
            "pokemon.Pokemon",
            attack=60, defense=45, hp=50, _quantity=3)

        pokemons = [pokemon_1, pokemon_2, pokemon_3]

        for count, pokemon in enumerate(pokemons):
            PokemonTeam.objects.create(
                team=team_creator,
                pokemon=pokemon,
                order=count)

        for count, pokemon in enumerate(pokemons):
            PokemonTeam.objects.create(
                team=team_opponent,
                pokemon=pokemon,
                order=count)

        result_battle_mock.return_value = team_creator
        run_battle_and_send_result_email.apply([battle.id])
        result_battle_mock.assert_called_with(battle)


class IntegrationPokeapiTest(TestCase):
    def test_if_pokeapi_integration_returns_pokemon_data_sucessfully(self):
        fake_json = {
            "defense": 40,
            "attack": 55,
            "hp": 35,
            "name": 'pikachu',
            "img_url": 'https://raw.githubusercontent.com'
                       '/PokeAPI/sprites/master/sprites/pokemon/25.png',
            "pokemon_id": 25,
        }

        with patch("pokemon.helpers.requests") as mock_get:
            mock_get.return_value.json.return_value = fake_json

        response = get_pokemon_from_api('pikachu')

        self.assertEqual(response, fake_json)

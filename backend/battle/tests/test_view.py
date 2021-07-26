from django.test import TestCase, Client
from django.conf import settings
from unittest.mock import patch
from model_bakery import baker
from django.urls import reverse
from users.models import User
from battle.models import Battle
from pokemon.helpers import get_pokemon_from_api


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
            "opponent": self.opponent.id,
        }
        self.client.login(username=self.creator.email, password='admin')
        self.client.post(reverse('battle'), battle_data)
        battle = Battle.objects.filter(creator=self.creator, opponent=self.opponent)
        self.assertTrue(battle)

    def test_if_returns_error_when_creator_and_opponent_are_the_same_user(self):
        battle_data = {
            "creator": self.creator.id,
            "opponent": self.creator.id,
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
            "opponent": self.opponent.id,
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


class IntegrationPokeapiTest(TestCase):
    def test_if_pokeapi_integration_returns_pokemon_data_sucessfully(self):
        fake_json = {
            "defense": 40,
            "attack": 55,
            "hp": 35,
            "name": 'pikachu',
            "img_url": 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png',
            "pokemon_id": 25,
        }

        with patch("pokemon.helpers.requests") as mock_get:
            mock_get.return_value.json.return_value = fake_json

        response = get_pokemon_from_api('pikachu')

        self.assertEqual(response, fake_json)

from unittest.mock import patch
from model_bakery import baker
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from django.conf import settings
from battle.models import Battle, Team
from battle.serializers import BattleSerializer


class APITestCaseUtils(APITestCase):
    def setUp(self):
        self.user_1 = baker.make("users.User")
        self.opponent = baker.make("users.User")

        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user_1)


class ListBattleEndpointTest(APITestCaseUtils):

    def test_login_user_can_acess_battle_list(self):
        response = self.auth_client.get(reverse('battle-list'))
        self.assertEqual(response.status_code, 200)

    def test_endpoint_returns_empty_list(self):
        response = self.auth_client.get(reverse('battle-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_endpoint_returns_one_battle_in_list(self):
        battle = baker.make('battle.Battle', creator=self.user_1)
        response = self.auth_client.get(reverse('battle-list'))
        matching_battles = BattleSerializer([battle], many=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(matching_battles.data, response.json())

    def test_endpoint_returns_few_battle_ids(self):
        battles = baker.make('battle.Battle', creator=self.user_1, _quantity=3)
        response = self.auth_client.get(reverse('battle-list'))
        matching_battles = BattleSerializer(battles, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(matching_battles.data, response.json())

    def test_endpoint_returns_a_lot_battle_ids(self):
        battles = baker.make('battle.Battle', creator=self.user_1, _quantity=100)
        response = self.auth_client.get(reverse('battle-list'))
        matching_battles = BattleSerializer(battles, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(matching_battles.data, response.json())

    def test_endpoint_returns_an_error_when_the_user_is_not_logged(self):
        self.auth_client.logout()
        response = self.client.get(reverse('battle-list'))
        self.assertEqual(response.status_code, 403)

    def test_endpoint_diff_to_verify_it_returns_exactly_len_of_battle_list(self):
        battles = baker.make('battle.Battle', creator=self.user_1, _quantity=10)

        response_initial = self.auth_client.get(reverse('battle-list'))

        self.assertCountEqual(BattleSerializer(battles, many=True).data, response_initial.json())

        baker.make('battle.Battle', creator=self.user_1, _quantity=50)

        all_battles = Battle.objects.filter(creator=self.user_1)

        response_updated = self.auth_client.get(reverse('battle-list'))

        self.assertCountEqual(
            BattleSerializer(all_battles, many=True).data,
            response_updated.json())


class DeatilBattleEndpointTest(APITestCaseUtils):

    def test_logged_user_can_acess_battle_detail(self):
        battle = baker.make("battle.Battle", creator=self.user_1, opponent=self.opponent)
        response = self.auth_client.get(reverse('battle-detail', kwargs={'pk': battle.id}))
        self.assertEqual(response.status_code, 200)

    def test_endpoint_returns_404_status(self):
        response = self.auth_client.get(reverse('battle-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)

    def test_endpoint_returns_404_status_when_acess_invalid_battle(self):
        battle = baker.make("battle.Battle")
        response = self.auth_client.get(reverse('battle-detail', kwargs={'pk': battle.id}))
        self.assertEqual(response.status_code, 404)

    def test_endpoint_returns_an_error_when_the_user_is_not_logged(self):
        self.auth_client.logout()
        response = self.auth_client.get(reverse('battle-detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 403)


class CreateBattleEndpointTest(APITestCaseUtils):

    def test_create_battle_successfully(self):
        battle_data = {
            "creator": self.user_1.id,
            "opponent": self.opponent.email,
        }
        response = self.auth_client.post(reverse('battle-create'), battle_data)
        battle = Battle.objects.filter(creator=self.user_1, opponent=self.opponent)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(battle)

    def test_if_returns_error_when_creator_and_opponent_are_the_same_user(self):
        battle_data = {
            "creator": self.user_1.id,
            "opponent": self.user_1.email,
        }
        response = self.auth_client.post(reverse('battle-create'), battle_data)
        self.assertEqual(
            response.json()['creator'][0],
            "ERROR: You can't challenge yourself.")

    def test_if_returns_error_when_opponent_doesnt_exist(self):
        battle_data = {
            "creator": self.user_1.id,
            "opponent": "",
        }
        response = self.auth_client.post(reverse('battle-create'), battle_data)
        self.assertEqual(
            response.json()['opponent'][0],
            'This field may not be blank.')

    @patch("battle.battles.email.send_templated_mail")
    def test_if_battle_invitation_email_is_sent(self, mock_templated_mail):
        battle_data = {
            "creator": self.user_1.id,
            "opponent": self.opponent.email,
        }

        self.auth_client.post(reverse("battle-create"), battle_data)

        mock_templated_mail.assert_called_with(
            template_name="invite_challenge",
            from_email=settings.FROM_EMAIL,
            recipient_list=[self.opponent.email],
            context={
                'creator': self.user_1.email,
            },
        )


class CreateTeamEndpointTest(APITestCaseUtils):
    def setUp(self):
        super().setUp()
        self.battle = baker.make('battle.Battle', creator=self.user_1)
        names = ['pikachu', 'bulbasaur', 'pidgeot', 'wrong_name']
        for pokemon_name in names:
            baker.make("pokemon.Pokemon", name=pokemon_name, attack=60, defense=15, hp=10)

    @patch('battle.views.run_battle_and_send_result_email.delay')
    def test_if_task_run_battle_is_called(self, task_mock):
        battle = Battle.objects.create(creator=self.user_1, opponent=self.opponent)

        pokemons_data_opponnent = {
            "battle": battle.id,
            "trainer": self.opponent.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        self.auth_client.post(
            reverse("team-create"), pokemons_data_opponnent, follow=True)
        self.assertTrue(Team.objects.get(battle=battle, trainer=self.opponent))

        pokemons_data = {
            "battle": battle.id,
            "trainer": self.user_1.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        self.auth_client.post(
            reverse("team-create"), pokemons_data, follow=True)

        task_mock.assert_called_with(battle.id)

        self.assertTrue(Team.objects.get(battle=battle, trainer=self.user_1))

    @patch('battle.battles.email.send_templated_mail')
    def test_if_task_send_email(self, email_mock):
        battle = Battle.objects.create(creator=self.user_1, opponent=self.opponent)

        pokemons_data_opponnent = {
            "battle": battle.id,
            "trainer": self.opponent.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        self.auth_client.post(
            reverse("team-create"), pokemons_data_opponnent, follow=True)
        self.assertTrue(Team.objects.get(battle=battle, trainer=self.opponent))

        pokemons_data = {
            "battle": battle.id,
            "trainer": self.user_1.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        self.auth_client.post(
            reverse("team-create"), pokemons_data, follow=True)

        battle_updated = Battle.objects.get(creator=self.user_1, opponent=self.opponent)

        email_mock.assert_called_with(
            template_name='results_battle',
            from_email=settings.FROM_EMAIL,
            recipient_list=[battle_updated.creator, battle_updated.opponent],
            context={
                'winner': battle_updated.winner,
            },
        )

    def test_user_can_create_team_with_pokemons(self):
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user_1.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        response = self.auth_client.post(
            reverse("team-create"), pokemons_data, follow=True)
        self.assertEqual(response.status_code, 201)

        team_user = Team.objects.get(battle=self.battle, trainer=self.user_1)
        self.assertTrue(team_user)

        pokemons_data_submited = {
            pokemons_data['pokemon_1'],
            pokemons_data['pokemon_2'],
            pokemons_data['pokemon_3']
        }

        self.assertEqual(
            pokemons_data_submited,
            {p.name for p in team_user.pokemons.all()}
        )

    def test_if_returns_error_when_type_wrong_pokemon_name(self):
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user_1.id,
            "pokemon_1": 'wrong_name',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        response = self.auth_client.post(
            reverse("team-create"),
            pokemons_data, follow=True)

        self.assertEqual(
            response.json()['non_field_errors'][0],
            'ERROR: Type the correct pokemons name')

    def test_if_returns_error_when_missing_position(self):
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user_1.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
        }
        response = self.auth_client.post(reverse(
            "team-create"), pokemons_data, follow=True)

        self.assertEqual(
            response.json()['non_field_errors'][0],
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
            reverse("team-create"),
            pokemons_data,
            follow=True)
        self.assertEqual(
            response.json()['detail'],
            'ERROR: You do not have permission for this action.')

    def test_if_returns_error_when_missing_pokemons(self):
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user_1.id,
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        response = self.auth_client.post(
            reverse("team-create"),
            pokemons_data,
            follow=True)
        self.assertEqual(
            response.json()['non_field_errors'][0],
            'ERROR: Select all pokemons')


class CurrentUserEndpointTest(APITestCaseUtils):

    def test_endpoint_returns_current_user(self):
        response = self.auth_client.get(reverse("current-user"))
        self.assertEqual(
            response.json()['email'],
            self.user_1.email)

    def test_endpoint_returns_error_if_user_is_not_logged(self):
        self.auth_client.logout()
        response = self.auth_client.get(reverse("current-user"))
        self.assertEqual(response.status_code, 403)

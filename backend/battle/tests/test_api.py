from model_bakery import baker
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from battle.models import Battle
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
        battle = baker.make('battle.Battle', creator=self.user_1)
        response = self.auth_client.get(reverse('battle-list'))
        matching_battles = BattleSerializer([battle], many=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(matching_battles.data, response.json())

    def test_endpoint_returns_one_battle_in_list(self):
        battle = baker.make('battle.Battle', creator=self.user_1)
        response = self.auth_client.get(reverse('battle-list'))
        matching_battles = BattleSerializer([battle], many=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(matching_battles.data, response.json())

    def test_endpoint_returns_few_battle_ids(self):
        battle = baker.make('battle.Battle', creator=self.user_1, _quantity=3)
        response = self.auth_client.get(reverse('battle-list'))
        matching_battles = BattleSerializer(battle, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(matching_battles.data, response.json())

    def test_endpoint_returns_a_lot_battle_ids(self):
        battle = baker.make('battle.Battle', creator=self.user_1, _quantity=100)
        response = self.auth_client.get(reverse('battle-list'))
        matching_battles = BattleSerializer(battle, many=True)
        self.assertEqual(response.status_code, 200)
        self.assertCountEqual(matching_battles.data, response.json())

    def test_endpoint_returns_an_error_when_the_user_is_not_logged(self):
        self.auth_client.logout()
        response = self.client.get(reverse('battle-list'))
        self.assertEqual(response.status_code, 403)

    def test_endpoint_diff_to_verify_it_returns_exactly_len_of_battle_list(self):
        battle = baker.make('battle.Battle', creator=self.user_1, _quantity=10)

        response_initial = self.auth_client.get(reverse('battle-list'))

        self.assertCountEqual(BattleSerializer(battle, many=True).data, response_initial.json())

        baker.make('battle.Battle', creator=self.user_1, _quantity=50)

        all_battles = Battle.objects.filter(creator=self.user_1)

        response_updated = self.auth_client.get(reverse('battle-list'))

        self.assertCountEqual(
            BattleSerializer(all_battles, many=True).data,
            response_updated.json())

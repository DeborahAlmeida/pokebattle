from unittest.mock import patch
from model_bakery import baker
from common.utils.tests import TestCaseUtils
from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError

from battle.models import Battle, PokemonTeam, Team
from battle.forms import TeamForm
from battle.battles.battle import get_winner_for, validate_sum_pokemons
from battle.tasks import run_battle_and_send_result_email


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
        self.assertCountEqual(response_qs, list(Battle.objects.filter(creator=self.user)))

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

    @patch("battle.battles.email.send_templated_mail")
    def test_if_battle_invitation_email_is_sent(self, mock_templated_mail):
        battle_data = {
            "creator": self.user.id,
            "opponent": self.opponent.email,
        }

        self.auth_client.post(reverse("battle"), battle_data)

        mock_templated_mail.assert_called_with(
            template_name="invite_challenge",
            from_email=settings.FROM_EMAIL,
            recipient_list=[self.opponent.email],
            context={
                'creator': self.user.email,
            },
        )


class IntegrationPokeApiTest(TestCaseUtils):

    @patch('battle.battles.battle.get_pokemon_from_api')
    def test_if_function_valid_points_returns_corretly(self, mock_get_pokemon):
        def side_effect_func(pokemon_name):
            fake_json = 1
            if pokemon_name == 'pikachu':
                fake_json = {
                    "defense": 40,
                    "attack": 55,
                    "hp": 35,
                    "name": 'pikachu',
                    "img_url": 'https://raw.githubusercontent.com'
                            '/PokeAPI/sprites/master/sprites/pokemon/25.png',
                    "pokemon_id": 25,
                }
            elif pokemon_name == 'pidgey':
                fake_json = {
                    "defense": 50,
                    "attack": 25,
                    "hp": 15,
                    "name": 'pidgey',
                    "img_url": 'https://raw.githubusercontent.com'
                            '/PokeAPI/sprites/master/sprites/pokemon/25.png',
                    "pokemon_id": 15,
                }
            elif pokemon_name == 'bulbasaur':
                fake_json = {
                    "defense": 30,
                    "attack": 40,
                    "hp": 20,
                    "name": 'bulbasaur',
                    "img_url": 'https://raw.githubusercontent.com'
                            '/PokeAPI/sprites/master/sprites/pokemon/25.png',
                    "pokemon_id": 10,
                }
            return fake_json
        mock_get_pokemon.side_effect = side_effect_func

        is_valid_sum = validate_sum_pokemons(['pikachu', 'pidgey', 'bulbasaur'])

        self.assertTrue(is_valid_sum)


class TeamViewTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.battle = baker.make('battle.Battle', creator=self.user)
        names = ['pikachu', 'bulbasaur', 'pidgeot', 'wrong_name']
        for pokemon_name in names:
            baker.make("pokemon.Pokemon", name=pokemon_name, attack=60, defense=15, hp=10)
        self.opponent = baker.make('users.User')

    @patch('battle.views.run_battle_and_send_result_email.delay')
    def test_if_task_run_battle_is_called(self, task_mock):
        battle = Battle.objects.create(creator=self.user, opponent=self.opponent)

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
            reverse("team_create", kwargs={'pk': battle.id}), pokemons_data_opponnent, follow=True)
        self.assertTrue(Team.objects.get(battle=battle, trainer=self.opponent))

        pokemons_data = {
            "battle": battle.id,
            "trainer": self.user.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        self.auth_client.post(
            reverse("team_create", kwargs={'pk': battle.id}), pokemons_data, follow=True)

        task_mock.assert_called_with(battle.id)

        self.assertTrue(Team.objects.get(battle=battle, trainer=self.user))

    @patch('battle.battles.email.send_templated_mail')
    def test_if_task_send_email(self, email_mock):
        battle = Battle.objects.create(creator=self.user, opponent=self.opponent)

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
            reverse("team_create", kwargs={'pk': battle.id}), pokemons_data_opponnent, follow=True)
        self.assertTrue(Team.objects.get(battle=battle, trainer=self.opponent))

        pokemons_data = {
            "battle": battle.id,
            "trainer": self.user.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        self.auth_client.post(
            reverse("team_create", kwargs={'pk': battle.id}), pokemons_data, follow=True)

        battle_updated = Battle.objects.get(creator=self.user, opponent=self.opponent)

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


class TeamFormTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.battle = baker.make('battle.Battle', creator=self.user)
        names = ['pikachu', 'bulbasaur', 'pidgeot', 'wrong_name']
        for pokemon_name in names:
            baker.make("pokemon.Pokemon", name=pokemon_name, attack=60, defense=15, hp=10)

    def test_form_is_valid(self):
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
        form = TeamForm(data=pokemons_data)
        self.assertTrue(form.is_valid())

    def test_form_saved_successfully(self):
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
        form = TeamForm(data=pokemons_data)
        self.assertTrue(form.is_valid())
        instance = form.save()
        self.assertEqual(Team.objects.get(battle=self.battle, trainer=self.user), instance)

    def test_form_returns_error_pokemons_missing(self):
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user.id,
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        form = TeamForm(data=pokemons_data)
        self.assertFalse(form.is_valid())
        with self.assertRaisesMessage(ValidationError, 'ERROR: Select all pokemons'):
            form.save()

    def test_form_returns_error_positions_missing(self):
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
        }
        form = TeamForm(data=pokemons_data)
        self.assertFalse(form.is_valid())
        with self.assertRaisesMessage(ValidationError, 'ERROR: Select all positions'):
            form.save()

    def test_form_returns_error_with_incorrect_pkn_name(self):
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user.id,
            "pokemon_1": 'pikachuuu',
            "pokemon_2": 'bulbasaurrr',
            "pokemon_3": 'pidgeottt',
            "position_pkn_1": 1,
            "position_pkn_2": 2,
            "position_pkn_3": 3,
        }
        form = TeamForm(data=pokemons_data)
        self.assertFalse(form.is_valid())
        with self.assertRaisesMessage(ValidationError, 'ERROR: Type the correct pokemons name'):
            form.save()

    def test_form_returns_error_with_same_positions(self):
        pokemons_data = {
            "battle": self.battle.id,
            "trainer": self.user.id,
            "pokemon_1": 'pikachu',
            "pokemon_2": 'bulbasaur',
            "pokemon_3": 'pidgeot',
            "position_pkn_1": 1,
            "position_pkn_2": 1,
            "position_pkn_3": 2,
        }
        form = TeamForm(data=pokemons_data)
        self.assertFalse(form.is_valid())
        with self.assertRaisesMessage(ValidationError, 'ERROR: You cannot add the same position'):
            form.save()

    def test_form_is_invalid_with_empty_data(self):
        form = TeamForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 9)


class TaskAsyncTest(TestCaseUtils):
    def setUp(self):
        super().setUp()
        self.opponent = baker.make('users.User')

    def test_if_task_set_winner_correctly(self):
        battle = Battle.objects.create(creator=self.user, opponent=self.opponent)

        team_creator = baker.make('battle.Team', battle=battle, trainer=self.user)
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

        run_battle_and_send_result_email(battle.id)
        self.assertEqual(
            self.user,
            Battle.objects.get(creator=self.user, opponent=self.opponent).winner)

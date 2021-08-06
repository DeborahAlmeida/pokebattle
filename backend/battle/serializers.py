from rest_framework import serializers
from battle.models import Battle, Team, PokemonTeam
from services.create_battle import (
    validate_if_creator_and_opponent_are_different,
    validate_if_opponent_is_valid, create_battle)
from services.create_team import verify_if_data_is_valid
from users.models import User

from battle.battles.battle import validate_sum_pokemons, verify_pokemon_is_saved

from pokemon.models import Pokemon
from pokemon.helpers import verify_pokemon_exists_api

POSITION_CHOICES = [(1, 1), (2, 2), (3, 3)]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id")

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ("id", "battle", "trainer", "pokemons")


class TeamCreateSerializer(serializers.Serializer):

    battle = serializers.PrimaryKeyRelatedField(queryset=Battle.objects.all())
    trainer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    pokemon_1 = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    pokemon_2 = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
    pokemon_3 = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

    position_pkn_1 = serializers.ChoiceField(
        choices=POSITION_CHOICES,
        label="Position",
        required=False)
    position_pkn_2 = serializers.ChoiceField(
        choices=POSITION_CHOICES,
        label="Position",
        required=False)
    position_pkn_3 = serializers.ChoiceField(
        choices=POSITION_CHOICES,
        label="Position",
        required=False)

    class Meta:
        model = Team
        fields = (
            "battle",
            "trainer",
            "position_pkn_1",
            "position_pkn_2",
            "position_pkn_3",
            "pokemon_1",
            "pokemon_2",
            "pokemon_3"
        )

    def validate(self, value):
        valid = verify_if_data_is_valid(value)
        if valid is not True:
            raise serializers.ValidationError(valid)
        return value

    def create(self, validated_data):

        pokemon_1 = self.validated_data['pokemon_1']
        pokemon_2 = self.validated_data['pokemon_2']
        pokemon_3 = self.validated_data['pokemon_3']

        pokemon_1_object = Pokemon.objects.get(name=pokemon_1)
        pokemon_2_object = Pokemon.objects.get(name=pokemon_2)
        pokemon_3_object = Pokemon.objects.get(name=pokemon_3)

        position_pkn_1 = self.validated_data['position_pkn_1']
        position_pkn_2 = self.validated_data['position_pkn_2']
        position_pkn_3 = self.validated_data['position_pkn_3']

        validated_data.pop('pokemon_1')
        validated_data.pop('pokemon_2')
        validated_data.pop('pokemon_3')
        validated_data.pop('position_pkn_1')
        validated_data.pop('position_pkn_2')
        validated_data.pop('position_pkn_3')

        instance = Team.objects.create(**validated_data)

        PokemonTeam.objects.create(
            team=instance,
            pokemon=pokemon_1_object,
            order=position_pkn_1)

        PokemonTeam.objects.create(
            team=instance,
            pokemon=pokemon_2_object,
            order=position_pkn_2)

        PokemonTeam.objects.create(
            team=instance,
            pokemon=pokemon_3_object,
            order=position_pkn_3)

        return instance













    # def create(self, validated_data):
    #     print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", validated_data)
    #     instance = Team.objects.create(**validated_data)
    #     return instance

'''
        PokemonTeam.objects.create(
            team=instance,
            pokemon=self.initial_data['pokemon_1_object'],
            order=self.initial_data['position_pkn_1'])

        PokemonTeam.objects.create(
            team=instance,
            pokemon=self.initial_data['pokemon_2_object'],
            order=self.initial_data['position_pkn_2'])

        PokemonTeam.objects.create(
            team=instance,
            pokemon=self.initial_data['pokemon_3_object'],
            order=self.initial_data['position_pkn_3'])
'''

class BattleSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Battle
        fields = ("id", "creator", "opponent", "winner", "teams")


class BattleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Battle
        fields = ("id", "creator", "opponent", "winner")

    def validate_creator(self, value):
        valid_field = validate_if_creator_and_opponent_are_different(
            self.initial_data['creator'], self.initial_data['opponent'])
        if not valid_field:
            raise serializers.ValidationError("ERROR: You can't challenge yourself.")
        return value

    def validate_opponent(self, value):
        if 'opponent' in self.initial_data:
            valid_opponent = validate_if_opponent_is_valid(self.initial_data['opponent'])
            value = valid_opponent
            value.is_guest = valid_opponent.is_guest
        else:
            raise serializers.ValidationError("ERROR: You need to choose an opponent")
        return value

    def create(self, validated_data):
        create_battle(self, validated_data['opponent'], validated_data['creator'])
        return Battle.objects.create(**validated_data)

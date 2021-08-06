from rest_framework import serializers
from battle.models import Battle, Team
from services.create_battle import (
    validate_if_creator_and_opponent_are_different,
    validate_if_opponent_is_valid, create_battle)
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id")


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ("id", "battle", "trainer", "pokemons")


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

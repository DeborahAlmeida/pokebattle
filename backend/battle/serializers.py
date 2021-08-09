from rest_framework import serializers
from battle.models import Battle, Team
from services.create_battle import (
    validate_if_creator_and_opponent_has_different_contenders,
    fetch_opponent_or_create_if_doenst_exist, send_invite_email_or_create_password_email)
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
        valid_field = validate_if_creator_and_opponent_has_different_contenders(
            self.initial_data['creator'], self.initial_data['opponent'])
        if not valid_field:
            raise serializers.ValidationError("ERROR: You can't challenge yourself.")
        return value

    def validate_opponent(self, value):
        if 'opponent' in self.initial_data:
            valid_opponent = fetch_opponent_or_create_if_doenst_exist(self.initial_data['opponent'])
            value = valid_opponent
            value.is_guest = valid_opponent.is_guest
        else:
            raise serializers.ValidationError("ERROR: You need to choose an opponent")
        return value

    def create(self, validated_data):
        send_invite_email_or_create_password_email(
            self,
            validated_data['opponent'],
            validated_data['creator'])
        return Battle.objects.create(**validated_data)

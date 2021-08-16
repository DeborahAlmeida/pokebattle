from rest_framework import serializers

from battle.models import Battle, Team, PokemonTeam
from battle.tasks import run_battle_and_send_result_email
from battle.battles.battle import save_pokemons_if_they_dont_exist

from services.battle import (
    has_pokemons_fields_missing_values,
    has_fields_with_wrong_pokemon_name,
    has_positions_fields_missing_values,
    has_pokemon_sum_valid,
    has_positions_fields_with_duplicate_values,
    has_different_contenders,
    fetch_opponent_or_create_if_doesnt_exist,
    send_invite_email_or_send_password_email
)

from users.models import User

from pokemon.models import Pokemon

POSITION_CHOICES = [(1, 1), (2, 2), (3, 3)]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "id")


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ("id", "battle", "trainer", "pokemons")


class TeamCreateSerializer(serializers.Serializer):  # pylint: disable=abstract-method

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

    def validate(self, attrs):

        if Team.objects.filter(battle=attrs['battle'], trainer=attrs['trainer']).exists():
            raise serializers.ValidationError('You cannot create a new team for this battle')

        valid = has_pokemons_fields_missing_values(attrs)
        if valid is not True:
            raise serializers.ValidationError('ERROR: Select all pokemons')

        valid = has_positions_fields_missing_values(attrs)
        if valid is not True:
            raise serializers.ValidationError('ERROR: Select all positions')

        valid = has_fields_with_wrong_pokemon_name(attrs)
        if valid is not True:
            raise serializers.ValidationError('ERROR: Type the correct pokemons name')

        valid = has_pokemon_sum_valid(attrs)
        if valid is not True:
            raise serializers.ValidationError(
                'ERROR: Pokemons sum more than 600 points. Select again'
            )

        valid = has_positions_fields_with_duplicate_values(attrs)
        if valid is not True:
            raise serializers.ValidationError('ERROR: You cannot add the same position')

        save_pokemons_if_they_dont_exist(
            [
                attrs['pokemon_1'],
                attrs['pokemon_2'],
                attrs['pokemon_3']
            ]
        )
        return attrs

    def create(self, validated_data):

        pokemon_1 = validated_data.pop('pokemon_1')
        pokemon_2 = validated_data.pop('pokemon_2')
        pokemon_3 = validated_data.pop('pokemon_3')

        pokemon_1_object = Pokemon.objects.get(name=pokemon_1)
        pokemon_2_object = Pokemon.objects.get(name=pokemon_2)
        pokemon_3_object = Pokemon.objects.get(name=pokemon_3)

        position_pkn_1 = validated_data.pop('position_pkn_1')
        position_pkn_2 = validated_data.pop('position_pkn_2')
        position_pkn_3 = validated_data.pop('position_pkn_3')

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

        if len(validated_data['battle'].teams.all()) == 2:
            run_battle_and_send_result_email.delay(validated_data['battle'].id)
        return instance


class BattleSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Battle
        fields = ("id", "creator", "opponent", "winner", "teams")


class BattleCreateSerializer(serializers.ModelSerializer):
    opponent = serializers.CharField(style={'base_template': 'textarea.html'})

    class Meta:
        model = Battle
        fields = ("id", "creator", "opponent", "winner")

    def validate_creator(self, value):
        valid_field = has_different_contenders(
            self.initial_data['creator'], self.initial_data['opponent'])
        if not valid_field:
            raise serializers.ValidationError("ERROR: You can't challenge yourself.")
        return value

    def validate_opponent(self, value):
        if 'opponent' not in self.initial_data:
            raise serializers.ValidationError("ERROR: You need to choose an opponent")
        value = fetch_opponent_or_create_if_doesnt_exist(self.initial_data['opponent'])
        return value

    def create(self, validated_data):
        send_invite_email_or_send_password_email(
            validated_data['opponent'],
            validated_data['creator'])
        return Battle.objects.create(**validated_data)

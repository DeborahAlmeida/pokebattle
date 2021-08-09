from django import forms
from django.contrib.auth.forms import UserCreationForm

from battle.models import Battle, PokemonTeam, Team
from battle.battles.battle import validate_sum_pokemons, verify_pokemon_is_saved

from users.models import User

from pokemon.models import Pokemon

from pokemon.helpers import verify_pokemon_exists_api

from services.create_battle import (
    validate_if_creator_and_opponent_has_different_contenders,
    fetch_opponent_or_create_if_doenst_exist, send_invite_email_or_create_password_email)

POSITION_CHOICES = [(1, 1), (2, 2), (3, 3)]


class BattleForm(forms.ModelForm):
    opponent = forms.EmailField()

    class Meta:
        model = Battle
        fields = ['creator', 'opponent', ]

    def __init__(self, *args, **kwargs):
        super(BattleForm, self).__init__(*args, **kwargs)
        self.fields['creator'].widget = forms.HiddenInput()

    def clean_opponent(self):
        opponent = fetch_opponent_or_create_if_doenst_exist(self.cleaned_data['opponent'])
        return opponent

    def clean(self):
        cleaned_data = super().clean()
        if 'creator' not in cleaned_data:
            raise forms.ValidationError("ERROR: You need to be logged.")

        if 'opponent' not in cleaned_data:
            raise forms.ValidationError("ERROR: You need to choose an opponent")

        valid_creator_field = validate_if_creator_and_opponent_has_different_contenders(
            cleaned_data['opponent'], cleaned_data['creator'])

        if not valid_creator_field:
            raise forms.ValidationError("ERROR: You can't challenge yourself.")
        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.clean()
        instance = super().save()
        opponent = cleaned_data["opponent"]
        send_invite_email_or_create_password_email(self, opponent, instance.creator)
        return instance


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "battle",
            "trainer",
            "pokemon_1",
            "pokemon_2",
            "pokemon_3",
            "position_pkn_1",
            "position_pkn_2",
            "position_pkn_3",
        ]

    battle = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=Battle.objects.all())
    trainer = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects.all())
    position_pkn_1 = forms.ChoiceField(choices=POSITION_CHOICES, label="Position")
    position_pkn_2 = forms.ChoiceField(choices=POSITION_CHOICES, label="Position")
    position_pkn_3 = forms.ChoiceField(choices=POSITION_CHOICES, label="Position")
    pokemon_1 = forms.CharField(widget=forms.Textarea)
    pokemon_2 = forms.CharField(widget=forms.Textarea)
    pokemon_3 = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()

        if 'battle' not in cleaned_data:
            raise forms.ValidationError('ERROR: Select a valid battle')

        obj_battle = cleaned_data['battle']
        obj_trainer = cleaned_data['trainer']

        if ('pokemon_1' or 'pokemon_2' or 'pokemon_3') not in cleaned_data:
            raise forms.ValidationError('ERROR: Select all pokemons')

        pokemon_1 = self.cleaned_data.get('pokemon_1')
        pokemon_2 = self.cleaned_data.get('pokemon_2')
        pokemon_3 = self.cleaned_data.get('pokemon_3')

        if ('position_pkn_1' or 'position_pkn_2' or 'position_pkn_3') not in cleaned_data:
            raise forms.ValidationError('ERROR: Select all positions')

        position_pkn_1 = cleaned_data['position_pkn_1']
        position_pkn_2 = cleaned_data['position_pkn_2']
        position_pkn_3 = cleaned_data['position_pkn_3']

        pokemons_exist = verify_pokemon_exists_api([pokemon_1, pokemon_2, pokemon_3])
        if not pokemons_exist:
            raise forms.ValidationError('ERROR: Type the correct pokemons name')

        valid_pokemons = validate_sum_pokemons(
            [
                cleaned_data['pokemon_1'],
                cleaned_data['pokemon_2'],
                cleaned_data['pokemon_3']
            ]
        )
        if obj_trainer not in (obj_battle.creator, obj_battle.opponent):
            raise forms.ValidationError("ERROR: You do not have permission for this action.")

        if not valid_pokemons:
            raise forms.ValidationError("ERROR: Pokemons sum more than 600 points. Select again.")

        if position_pkn_1 in (position_pkn_2, position_pkn_3):
            raise forms.ValidationError('ERROR: You cannot add the same position')
        if position_pkn_2 == position_pkn_3:
            raise forms.ValidationError('ERROR: You cannot add the same position')

        verify_pokemon_is_saved(
            [
                cleaned_data['pokemon_1'],
                cleaned_data['pokemon_2'],
                cleaned_data['pokemon_3']
            ]
        )
        cleaned_data['pokemon_1_object'] = Pokemon.objects.get(name=cleaned_data['pokemon_1'])
        cleaned_data['pokemon_2_object'] = Pokemon.objects.get(name=cleaned_data['pokemon_2'])
        cleaned_data['pokemon_3_object'] = Pokemon.objects.get(name=cleaned_data['pokemon_3'])
        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.clean()
        instance = super().save()

        PokemonTeam.objects.create(
            team=instance,
            pokemon=cleaned_data['pokemon_1_object'],
            order=cleaned_data['position_pkn_1'])

        PokemonTeam.objects.create(
            team=instance,
            pokemon=cleaned_data['pokemon_2_object'],
            order=cleaned_data['position_pkn_2'])

        PokemonTeam.objects.create(
            team=instance,
            pokemon=cleaned_data['pokemon_3_object'],
            order=cleaned_data['position_pkn_3'])
        return instance


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )

from django import forms
from django.contrib.auth.forms import UserCreationForm

from battle.models import Battle, PokemonTeam, Team

from users.models import User

from pokemon.models import Pokemon

from services.create_battle import (
    validate_if_creator_and_opponent_are_different,
    validate_if_opponent_is_valid, create_battle)

from services.create_team import verify_if_data_is_valid

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
        opponent = validate_if_opponent_is_valid(self.cleaned_data['opponent'])
        return opponent

    def clean(self):
        cleaned_data = super().clean()
        if 'creator' not in cleaned_data:
            raise forms.ValidationError("ERROR: You need to be logged.")

        if 'opponent' not in cleaned_data:
            raise forms.ValidationError("ERROR: You need to choose an opponent")

        valid_creator_field = validate_if_creator_and_opponent_are_different(
            cleaned_data['opponent'], cleaned_data['creator'])

        if not valid_creator_field:
            raise forms.ValidationError("ERROR: You can't challenge yourself.")
        return cleaned_data

    def save(self, commit=True):
        cleaned_data = self.clean()
        instance = super().save()
        opponent = cleaned_data["opponent"]
        create_battle(self, opponent, instance.creator)
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

        valid = verify_if_data_is_valid(cleaned_data)
        if valid is not True:
            raise forms.ValidationError(valid)

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
